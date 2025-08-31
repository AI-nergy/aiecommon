import asyncio
import aiecommon.custom_logger as custom_logger
logger = custom_logger.get_logger()

import json
import os, time, datetime, threading, queue, boto3
from typing import Optional

class AwsMetricEmitterBase:
    def __init__(
        self,
        namespace: str,
        metric_name: str,
        region_name: str,
        dimensions: list,
        flush_interval: float = 1.0,     # seconds
        max_batch: int = 1              # CW allows up to 20 metrics per PutMetricData
    ):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.flush_interval = flush_interval
        self.max_batch = max_batch
        logger.info("AwsMetricEmitterBase: Start AWS cloudwatch client")
        self._cw = boto3.client("cloudwatch", region_name=region_name)

        # logger.info("AwsMetricEmitterBase: Setup threading and queue")
        # self.queue: "queue.Queue[dict]" = queue.Queue()
        # self._stop = threading.Event()
        # self._thread = threading.Thread(target=self._run, name="cw-metrics", daemon=True)
        # self._thread.start()

    def _run(self):
        buf = []
        last_flush = time.time()
        while not self._stop.is_set():
            timeout = max(0.0, self.flush_interval - (time.time() - last_flush))
            try:
                item = self.queue.get(timeout=timeout)
                buf.append(item)
                # drain up to max_batch without blocking
                while len(buf) < self.max_batch:
                    try:
                        buf.append(self.queue.get_nowait())
                    except queue.Empty:
                        break
            except queue.Empty:
                pass

            # flush if interval expired or batch full
            if buf and (time.time() - last_flush >= self.flush_interval or len(buf) >= self.max_batch):
                try:
                    self._cw.put_metric_data(Namespace=self.namespace, MetricData=buf[:self.max_batch])
                except Exception:
                    pass
                finally:
                    # drop what we sent
                    del buf[:self.max_batch]
                    last_flush = time.time()

    def emit_metric(self, value: int):
        logger.info(f"AwsMetricEmitterBase: emit_metric, metric_name={self.metric_name}, value={value}")
        asyncio.create_task(asyncio.to_thread(self._emit_metric, value))

    def _emit_metric(self, value: int):
        try:
            self._cw.put_metric_data(
                Namespace=self.namespace,
                MetricData=[{
                    "MetricName": self.metric_name,
                    "Dimensions": self.dimensions,
                    "Timestamp": datetime.datetime.now(datetime.timezone.utc),
                    "Value": value,
                    "Unit": "Count",
                    "StorageResolution": 1,
                }]
            )
        except Exception as e:
            logger.exception(f"Failed to put metric metric_name={self.metric_name}, value=[value], exception={e}")

    def emit_metric_async(self, value: int):
        if not self.metric_name:
            return
        
        try:
            self.queue.put_nowait({
                "MetricName": self.metric_name,
                "Dimensions": self.dimensions,
                "Timestamp": datetime.datetime.now(datetime.timezone.utc),
                "Value": value,
                "Unit": "Count",
                "StorageResolution": 1,
            })
        except Exception:
            pass

    def shutdown(self, timeout: float = 2.0):
        self._stop.set()
        self._thread.join(timeout=timeout)
        if not self.metric_name:
            return

        # best-effort final flush
        try:
            remaining = []
            while True:
                remaining.append(self.queue.get_nowait())
        except queue.Empty:
            if remaining:
                try:
                    self._cw.put_metric_data(Namespace=self.namespace, MetricData=remaining[:min(self.max_batch, 20)])
                except Exception:
                    pass


class AwsEcsMetricEmitter(AwsMetricEmitterBase):

    # def __new__(cls, *args, **kwargs):
    #     cluster_info = cls.get_cluster_info()
    #     if cluster_info:
    #         instance = super().__new__(cls)
    #         instance.cluster_info = cluster_info
    #         return instance
    #     else:
    #         return None

    def __init__(
        self,
        namespace: str,
        metric_name: str,
        flush_interval: float = 1.0,     # seconds
        max_batch: int = 1              # CW allows up to 20 metrics per PutMetricData
    ):
        self.metric_name = None

        logger.info("AwsEcsMetricEmitter: get_cluster_info")
        self.cluster_info = self.get_cluster_info()

        if self.cluster_info:
            self.cluster_name = self.cluster_info["Cluster"]
            self.task_arn = self.cluster_info["TaskARN"]
            self.task_id = self.task_arn.split("/")[-1]
            # self.region = cluster_info["AvailabilityZone"]
            # self.region_name = None
            self.region_name = "eu-north-1"

            # self.service_name = os.getenv("ECS_SERVICE_NAME")
            logger.info("AwsEcsMetricEmitter: Get ECS service")
            ecs = boto3.client("ecs", region_name=self.region_name)
            resp = ecs.describe_tasks(cluster=self.cluster_name, tasks=[self.task_arn])
            group = resp["tasks"][0].get("group")
            self.service_name = group.split(":")[1] if group and group.startswith("service:") else None

            logger.info("AwsEcsMetricEmitter: Init metrics")
            super().__init__(
                namespace=namespace,
                region_name=self.region_name,
                metric_name=metric_name,
                dimensions=[
                    {"Name": "Cluster", "Value": self.cluster_name},
                    {"Name": "Service", "Value": self.service_name},
                    {"Name": "TaskId",  "Value": self.task_id},
                ],
                # dimensions=[{
                #     "Service": self.service_name,
                #     "Cluster": self.cluster_name,
                #     "TaskId": self.task_id
                # }],
                flush_interval=flush_interval,
                max_batch=max_batch
            )

    @staticmethod
    def get_cluster_info():
        metadata_file_path = os.getenv("ECS_CONTAINER_METADATA_FILE")

        try:
            with open(metadata_file_path, "r") as file:
                return json.load(file)
        except:
            return None

class MetricEmitter(AwsEcsMetricEmitter):
    pass
