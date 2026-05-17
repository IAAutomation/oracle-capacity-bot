import os
import sys
import requests
import oci
from oci.exceptions import ServiceError

# =========================================================
# ORACLE OCI CONFIG
# =========================================================

config = {
    "user": "ocid1.user.oc1..aaaaaaaacn36y6qx6cu4ldjefc2qbu7yaa5t2arc3yvbzt7abzjtwls4i7ha",

    "fingerprint": os.environ["OCI_FINGERPRINT"],

    "tenancy": "ocid1.tenancy.oc1..aaaaaaaaxh2rr7l5fgr3wpsxjv2gddobecb2klfiboaa7nu3ry32qutzvihq",

    "region": "me-dubai-1",

    "key_content": os.environ["OCI_PRIVATE_KEY"]
}

# =========================================================
# TELEGRAM CONFIG
# =========================================================

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(message):

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }

        requests.post(url, data=data)

    except Exception as e:
        print("Telegram Error:", e)

# =========================================================
# OCI CLIENT
# =========================================================

compute_client = oci.core.ComputeClient(config)

# =========================================================
# STATIC OCI VALUES
# =========================================================

COMPARTMENT_ID = "ocid1.tenancy.oc1..aaaaaaaaxh2rr7l5fgr3wpsxjv2gddobecb2klfiboaa7nu3ry32qutzvihq"

SUBNET_ID = "ocid1.subnet.oc1.me-dubai-1.aaaaaaaad27ivni7hdkuznhsgdavuaqidm3xv5naihq5w4dly4zl7dx2fbka"

AVAILABILITY_DOMAIN = "TnTd:ME-DUBAI-1-AD-1"

SSH_PUBLIC_KEY = os.environ["OCI_SSH_PUBLIC_KEY"]

# =========================================================
# INSTANCE SETTINGS
# =========================================================

INSTANCE_NAME = "openclaw-arm"

SHAPE = "VM.Standard.A1.Flex"

BOOT_VOLUME_SIZE = 50

# =========================================================
# CONFIG PRIORITY
# First tries 6GB
# Then tries 4GB
# =========================================================

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




# =========================================================
# FIND UBUNTU ARM IMAGE
# =========================================================

print("Searching for Ubuntu ARM image...")

send_telegram(
    "Oracle Retry Bot Started\n\nSearching for Ubuntu ARM image..."
)

images = compute_client.list_images(
    compartment_id=COMPARTMENT_ID
).data

IMAGE_ID = None

for image in images:

    name = image.display_name.lower()

    if (
        "ubuntu" in name and
        "22.04" in name and
        "aarch64" in name and
        "minimal" in name and
        image.lifecycle_state == "AVAILABLE"
    ):

        IMAGE_ID = image.id

        print(f"Found Image: {image.display_name}")
        print(f"Image ID: {IMAGE_ID}")

        break

if not IMAGE_ID:

    error_msg = "ERROR: Ubuntu ARM image not found"

    print(error_msg)

    send_telegram(error_msg)

    sys.exit(1)
# =========================================================
# TRY INSTANCE CREATION
# =========================================================

for cfg in INSTANCE_CONFIGS:

    ocpus = cfg["ocpus"]
    memory = cfg["memory"]

    print("\n===================================")
    print(f"Trying: {ocpus} OCPU / {memory} GB RAM")
    print("===================================\n")

    send_telegram(
        f"Oracle Capacity Attempt\n\nTrying:\n{ocpus} OCPU\n{memory}GB RAM"
    )

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

        success_msg = f'''
SUCCESS! ORACLE VM CREATED

Instance Name:
{INSTANCE_NAME}

Shape:
{SHAPE}

Config:
{ocpus} OCPU / {memory}GB RAM

Instance ID:
{instance_id}

IMPORTANT:
Disable GitHub workflow now.
'''

        print(success_msg)

        send_telegram(success_msg)

        sys.exit(0)

    except ServiceError as e:

        error_text = str(e.message)

        print("\nFAILED:")
        print(error_text)

        send_telegram(
            f"FAILED\n\n{ocpus} OCPU / {memory}GB\n\n{error_text}"
        )

        if "Out of capacity" in error_text:

            print("Capacity unavailable. Trying next config...")

        else:

            print("OCI API Error")

    except Exception as e:

        unexpected_error = str(e)

        print("\nUNEXPECTED ERROR:")
        print(unexpected_error)

        send_telegram(
            f"UNEXPECTED ERROR\n\n{unexpected_error}"
        )

# =========================================================
# ALL CONFIGS FAILED
# =========================================================

final_msg = '''
NO ORACLE CAPACITY AVAILABLE

Tried:
- 1 OCPU / 6GB
- 1 OCPU / 4GB

GitHub Actions will retry automatically in 5 minutes.
'''

print(final_msg)

send_telegram(final_msg)
