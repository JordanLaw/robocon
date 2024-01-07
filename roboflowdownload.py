from roboflow import Roboflow

rf = Roboflow(api_key="eU8NcpayJaDlSKKHTssC")
project = rf.workspace("vtc-4wrns").project("test-sjxjk")
dataset = project.version(2).download("yolov8")
