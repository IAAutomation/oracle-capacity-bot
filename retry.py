import oci
import time
import sys
import requests

# =========================================================
# OCI CONFIG
# =========================================================

USER_OCID = "ocid1.user.oc1..aaaaaaaacn36y6qx6cu4ldjefc2qbu7yaa5t2arc3yvbzt7abzjtwls4i7ha"

TENANCY_OCID = "ocid1.tenancy.oc1..aaaaaaaaxh2rr7l5fgr3wpsxjv2gddobecb2klfiboaa7nu3ry32qutzvihq"

COMPARTMENT_OCID = "ocid1.tenancy.oc1..aaaaaaaaxh2rr7l5fgr3wpsxjv2gddobecb2klfiboaa7nu3ry32qutzvihq"

SUBNET_OCID = "ocid1.subnet.oc1.me-dubai-1.aaaaaaaad27ivni7hdkuznhsgdavuaqidm3xv5naihq5w4dly4zl7dx2fbka"

REGION = "me-dubai-1"

AVAILABILITY_DOMAIN = "TnTd:ME-DUBAI-1-AD-1"

SHAPE = "VM.Standard.A1.Flex"

INSTANCE_NAME = "openclaw-arm"

# =========================================================
# IMAGE
# =========================================================

IMAGE_ID = "ocid1.image.oc1.me-dubai-1.aaaaaaaab352mbi4vcyymzs4ccln576k34khc357fk2hlaqx3cuzjclgkoea"

# =========================================================
# GITHUB SECRETS
# =========================================================

import os

FINGERPRINT = os.environ["OCI_FINGERPRINT"]

PRIVATE_KEY = os.environ["OCI_PRIVATE_KEY"]

SSH_PUBLIC_KEY = os.environ["OCI_SSH_PUBLIC_KEY"]

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# =========================================================
# TELEGRAM
# =========================================================

def send_telegram(message):

    try:

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=20
        )

    except Exception as e:

        print("Telegram Error:")
        print(str(e))

# =========================================================
# OCI CLIENT CONFIG
# =========================================================

config = {
    "user": USER_OCID,
    "key_content": PRIVATE_KEY,
    "fingerprint": FINGERPRINT,
    "tenancy": TENANCY_OCID,
    "region": REGION
}

compute_client = oci.core.ComputeClient(config)

# =========================================================
# INSTANCE CONFIGS
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
# START MESSAGE
# =========================================================

print("Using Ubuntu ARM image...")
print(f"Image ID: {IMAGE_ID}")

send_telegram(
    "Oracle Retry Bot Started\n\n"
    "Ubuntu 24.04 ARM image selected successfully."
)

# =========================================================
# TRY INSTANCE CREATION
# =========================================================

success = False

for config_item in INSTANCE_CONFIGS:

    ocpus = config_item["ocpus"]
    memory = config_item["memory"]

    print("===================================")
    print(f"Trying: {ocpus} OCPU / {memory} GB RAM")
    print("===================================")

    send_telegram(
        f"Trying Oracle VM:\n\n"
        f"OCPU: {ocpus}\n"
        f"RAM: {memory} GB"
    )

    try:

        launch_details = oci.core.models.LaunchInstanceDetails(

            compartment_id=COMPARTMENT_OCID,

            availability_domain=AVAILABILITY_DOMAIN,

            display_name=INSTANCE_NAME,

            shape=SHAPE,

            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
                ocpus=ocpus,
                memory_in_gbs=memory
            ),

            create_vnic_details=oci.core.models.CreateVnicDetails(
                subnet_id=SUBNET_OCID,
                assign_public_ip=True
            ),

            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=IMAGE_ID
            ),

            metadata={
                "ssh_authorized_keys": SSH_PUBLIC_KEY
            }
        )

        response = compute_client.launch_instance(
            launch_details
        )

        instance_id = response.data.id

        success = True

        print("===================================")
        print("SUCCESS! ORACLE VM CREATED")
        print(f"Instance ID: {instance_id}")
        print("===================================")

        send_telegram(
            "SUCCESS! ORACLE VM CREATED\n\n"
            f"Instance ID:\n{instance_id}\n\n"
            "Disable GitHub workflow now."
        )

        break

    except Exception as e:

        error_message = str(e)

        print("FAILED:")
        print(error_message)

        send_telegram(
            f"FAILED:\n\n"
            f"{error_message}"
        )

        time.sleep(60)

# =========================================================
# FINAL STATUS
# =========================================================

if not success:

    print("===================================")
    print("NO ORACLE CAPACITY AVAILABLE")
    print("")
    print("Tried:")
    print("- 1 OCPU / 6GB")
    print("- 1 OCPU / 4GB")
    print("")
    print("GitHub Actions will retry automatically in 10 minutes.")
    print("===================================")

    send_telegram(
        "NO ORACLE CAPACITY AVAILABLE\n\n"
        "Tried:\n"
        "- 1 OCPU / 6GB\n"
        "- 1 OCPU / 4GB\n\n"
        "Retrying automatically in 10 minutes."
    )

    sys.exit(0)
