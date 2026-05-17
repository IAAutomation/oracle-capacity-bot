import os
import sys
import time
import oci
from oci.exceptions import ServiceError

# =========================
# ORACLE OCI CONFIG
# =========================

config = {
    "user": "ocid1.user.oc1..aaaaaaaacn36y6qx6cu4ldjefc2qbu7yaa5t2arc3yvbzt7abzjtwls4i7ha",

    "fingerprint": os.environ["b0:ca:30:73:16:e5:a8:38:82:36:50:d3:c8:ff:57:d7"],

    "tenancy": "ocid1.tenancy.oc1..aaaaaaaaxh2rr7l5fgr3wpsxjv2gddobecb2klfiboaa7nu3ry32qutzvihq",

    "region": "me-dubai-1",

    "key_content": os.environ["-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDAxjI2cwRlGIrp
0rdypFN/hnQKJlhDJvyxeOUNqlwh7shlRJGIwQCAyvWaPinM8nWVi0RvZIwq4q2O
vbhPmwM1VQHuEZ/2rWynYR4FjfkvVIdNLSI508JfrbgIpHbtyFnYFtZGbwGAWU+u
CbD0Jwm47FONwNJ0PmTesyIHEyK+sWh9uNVWjbKGYHGK0lpodcinZF/n0ZbAskLP
wsAkczeAzlcbJ/lxHquc+9lDlPeO9bPyRadR0jtIKHkxxlCGATn14wfJSc3Wauma
jhqrjzugwmFInW4pyLPdpWARMv/NUC0oIVUOK9Y76W0wqNY+ptlrXa7ru8c3q67P
GOMeLbsfAgMBAAECggEAW37Wf0xo9hjHegJmypVfAiSNN/IKK1k6T3ubb7h/gSWF
3LbGQnukYvyxxHMjwOAFWiSfJyW4d3RePuUiMTpYM/x0bYvU+i5G50yrhKRldIbw
rvswhvTQiTv5ILT6s5JHvk3chtKSClqZfHeiEsfij/AvGhU+bijdFGw+RtBYydu0
XnE0Doe4ZkhqYFdwc9Rvi9m0usoQoEzqWWuAY18r6E9zIvGZhtn7DFeCf1gA46QG
87XfE9AOqwDzEPnMwTupqvrY/+oFECazZddVdJqY0e/zeGdk3YJEUFu8WRMjyrNm
IWAIYbTskmkpMb4hLk45CcaGEDVb546TokxKumpVhQKBgQDhtPNot79FyQoJwA1n
xXDgxPQeDLG/uSS2lxOY/8pu1p6f158g6TOCRVv/HGBR8lZVN5U4dc6sGGVffhwY
kkzYpL96Nj+GVJ+NjOtOv2lCXBlLZDI1EgvOY237ME6UNGY7FKPV1deJeOPnQNek
lQ4cIq3by2peoWwNHt/hTnF1PQKBgQDapbb0s8+wS8XCyihfaDhvaR3/R2m79TUx
V6aoLd5F1frNGVl2JjULJL/2ijFQ4deUny+QgJwbkO3mdT7CzQx4qyaffTKKe1b/
oBJHSZJGDNvFZTEHuspoUVuc4rUEKtsZmDgXPVKKWlAR9rgyIdOB5Emw6Gp+KaYl
0JFB+86PiwKBgA/y8GxK56ovvZTYzFmz2vkXEcT50qmglJaOcGUUViKk6cqTuvvh
XrFq40hQogHIZQ9agSHfOT5x7t/jkmquE94PLjSdlrmQS0H+XjZPUknNJkBskRus
7cakwgXI8RSJ61trZvRaSwO81iXmMBbCLaARV0W7xwVu1KrMrrdGCsBlAoGBAKS6
9XynfHJ2pCh95qz6+In3yIHsa90QgWMLhqRu6mfzL2IXFy/M2Wnr5jT5KO6nOKTg
yhU00Gh0aMiYzRA3LI49ZHwE928ePg2ZrCvJYkskpO+zrZ0FPjoaEcvBgmABadF+
vcPEj8ts/6aJG32pvpC+Tkba1GD5QBR9bvMnpBjBAoGBALzMLYOCg5j8sE1WPqD6
LChMyJ/bwQJ8IR8Co+jz0P0Ly2E8FfoN9PfUknwf4DR0Rq3ljjbIAzL6mUt6HLmj
WOtk6ZInPOmpCn8JJZRv7NTkOBnIHER2x4TitHIitsKtF35UwT3Yx1HQnlUFbnsM
ulvDsF2P71t5AY3bElz7TC5H
-----END PRIVATE KEY-----"]
}

# =========================
# OCI CLIENT
# =========================

compute_client = oci.core.ComputeClient(config)

# =========================
# STATIC VALUES
# =========================

COMPARTMENT_ID = "ocid1.tenancy.oc1..aaaaaaaaxh2rr7l5fgr3wpsxjv2gddobecb2klfiboaa7nu3ry32qutzvihq"

SUBNET_ID = "ocid1.subnet.oc1.me-dubai-1.aaaaaaaad27ivni7hdkuznhsgdavuaqidm3xv5naihq5w4dly4zl7dx2fbka"

AVAILABILITY_DOMAIN = "TnTd:ME-DUBAI-1-AD-1"

SSH_PUBLIC_KEY = os.environ["ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDSC0K5oQdse6BQkVFZ3iOqXS89GO/D3p0YS+mznHss/TjocOkd4YIGJdFgQIxrj+g2nIXWJLl38uhHjbtaNOz+2fIezlQbIDpUWkZ4C06IIbLWYW51GulUltFWctjdefuekLX+gIdvDYvBkLJrHZ2YbOFsQC9qDZf3VrsJcrslPd4cBz0lRfTSMz6xLzrrRsgT2/gwiFJUl4do//l6PV/SWzgmCOAaq/mSzLdKQ5PI8UEcUq/zp+ti2jyX4HnGJEb9qj9cACOCavk9iK78WgeTG4xykJ4FNPmmgtP1anRl9NlIHtrypFNPa3XbXgAeO2D3ri3JWk6koOyJP6IcxU9v ssh-key-2026-04-13"]

# =========================
# INSTANCE SETTINGS
# =========================

INSTANCE_NAME = "openclaw-arm"

SHAPE = "VM.Standard.A1.Flex"

BOOT_VOLUME_SIZE = 50

# =========================
# CONFIG PRIORITY
# First tries 6GB
# Then fallback to 4GB
# =========================

INSTANCE_CONFIGS = [
    {
        "ocpus": 1,
        "memory": 6
    },
    {
        "ocpus": 1,
        "memory": 4
    }
]

# =========================
# FIND UBUNTU ARM IMAGE
# =========================

print("Searching for Ubuntu ARM image...")

images = compute_client.list_images(
    compartment_id=COMPARTMENT_ID,
    operating_system="Canonical Ubuntu",
    operating_system_version="22.04"
).data

IMAGE_ID = None

for image in images:

    name = image.display_name.lower()

    if (
        "minimal" in name and
        "aarch64" in name and
        image.lifecycle_state == "AVAILABLE"
    ):
        IMAGE_ID = image.id

        print(f"Found Image: {image.display_name}")
        print(f"Image ID: {IMAGE_ID}")

        break

if not IMAGE_ID:
    print("ERROR: Ubuntu ARM image not found")
    sys.exit(1)

# =========================
# TRY INSTANCE CREATION
# =========================

for cfg in INSTANCE_CONFIGS:

    ocpus = cfg["ocpus"]
    memory = cfg["memory"]

    print("\n===================================")
    print(f"Trying: {ocpus} OCPU / {memory} GB RAM")
    print("===================================\n")

    try:

        launch_details = oci.core.models.LaunchInstanceDetails(
            compartment_id=COMPARTMENT_ID,

            availability_domain=AVAILABILITY_DOMAIN,

            display_name=INSTANCE_NAME,

            shape=SHAPE,

            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=ocpus,
                memory_in_gbs=memory
            ),

            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=IMAGE_ID,
                boot_volume_size_in_gbs=BOOT_VOLUME_SIZE
            ),

            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=SUBNET_ID,
                assign_public_ip=True
            ),

            metadata={
                "ssh_authorized_keys": SSH_PUBLIC_KEY
            }
        )

        response = compute_client.launch_instance(launch_details)

        instance_id = response.data.id

        print("\n===================================")
        print("SUCCESS! INSTANCE CREATED!")
        print("===================================\n")

        print(f"Instance ID: {instance_id}")

        sys.exit(0)

    except ServiceError as e:

        print("\nFAILED:")
        print(e.message)

        if "Out of capacity" in str(e):
            print("Capacity unavailable. Trying next config...")
        else:
            print("OCI Error occurred.")

    except Exception as e:

        print("\nUNEXPECTED ERROR:")
        print(str(e))

# =========================
# ALL CONFIGS FAILED
# =========================

print("\n===================================")
print("NO CAPACITY AVAILABLE")
print("GitHub Actions will retry later.")
print("===================================\n")
