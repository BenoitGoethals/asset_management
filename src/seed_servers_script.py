import os
import random
import uuid
import django

# 1. Set up Django environment BEFORE importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# 2. Now it's safe to import Django-related modules
from django.utils import timezone
from django.contrib.auth.models import User

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from asset.models import Server


def get_base_asset_data(i):
    """Generates random data for ALL BaseAsset attributes."""
    manufacturers = ['Dell', 'HP', 'Lenovo', 'Supermicro', 'Cisco', 'Apple', 'Microsoft']
    vendors = ['Insight', 'Bechtle', 'Softcat', 'Direct Vendor']
    buildings = ['Building A', 'Building B', 'HQ', 'West Wing']
    depts = ['IT', 'Finance', 'HR', 'Engineering', 'Sales']

    vendor_name = random.choice(manufacturers)
    asset_name = f"AST-{'SRV' if i % 2 == 0 else 'DEV'}-{random.randint(1000, 9999)}"

    # Get a random user for foreign keys (if any exist)
    user = User.objects.first()

    return {
        # Unique identifiers
        "asset_tag": f"TAG-{uuid.uuid4().hex[:8].upper()}",
        "serial_number": f"SN-{random.getrandbits(40)}",

        # Basic information
        "name": asset_name,
        "description": f"Generated asset for {asset_name} testing.",
        "manufacturer": vendor_name,
        "model": f"{vendor_name} Pro-Series v{random.randint(1, 5)}",
        "model_number": f"MN-{random.randint(100, 999)}X",

        # Network information
        "hostname": asset_name.lower(),
        "fqdn": f"{asset_name.lower()}.corp.internal",
        "primary_ip_address": f"10.10.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "secondary_ip_address": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "mac_address": "%02x:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(6)),
        "subnet_mask": "255.255.255.0",
        "default_gateway": "10.10.1.1",
        "dns_servers": "8.8.8.8, 1.1.1.1",
        "vlan_id": random.randint(10, 99),

        # Location information
        "physical_location": f"DataCenter-{random.choice(['Alpha', 'Beta', 'Gamma'])}",
        "building": random.choice(buildings),
        "floor": f"Floor {random.randint(1, 5)}",
        "room": f"Room {random.randint(100, 500)}",
        "rack_location": f"Rack-{random.randint(1, 42)}",
        "rack_unit": f"U{random.randint(1, 20)}",
        "geographic_location": "Amsterdam, NL",
        "site": "Main Campus",

        # Organizational
        "department": random.choice(depts),
        "cost_center": f"CC-{random.randint(1000, 9999)}",
        "business_unit": "Enterprise Infrastructure",
        "owner": user,
        "custodian": user,
        "assigned_to": user,

        # Lifecycle
        "purchase_date": timezone.now().date() - timezone.timedelta(days=random.randint(100, 1000)),
        "purchase_price": random.uniform(1000.0, 15000.0),
        "warranty_expiration": timezone.now().date() + timezone.timedelta(days=random.randint(100, 1000)),
        "vendor": random.choice(vendors),
        "purchase_order": f"PO-{random.randint(10000, 99999)}",

        # Status and compliance
        "status": random.choice(Server.Status.values),
        "environment": random.choice(Server.Environment.values),
        "risk_level": random.choice(Server.RiskLevel.values),
        "compliance_status": random.choice([True, False]),
        "authorized": True,
        "managed": True,

        # Security
        "encrypted": True,
        "encryption_method": "AES-256",
        "antivirus_installed": True,
        "antivirus_version": "v12.4.2",
        "firewall_enabled": True,
        "vulnerability_score": random.randint(0, 5),

        # Discovery
        "discovery_method": "Network Scan",
        "monitoring_enabled": True,

        # Metadata
        "notes": "Automatically seeded data for testing purposes.",
        "tags": "testing, automated, server",
        "configuration_items": {"last_audit": str(timezone.now().date()), "patch_group": "A"},
    }


def seed_servers(count=10):
    """Vult de database met een opgegeven aantal gegenereerde Servers met ALLE velden."""
    for i in range(count):
        data = get_base_asset_data(i)

        # Add Server-specific attributes
        data.update({
            # Server Info
            "server_type": random.choice(Server.ServerType.values),
            "operating_system": random.choice(Server.OperatingSystem.values),
            "os_version": f"v{random.randint(10, 22)}",
            "server_role": random.choice(Server.ServerRole.values),

            # Hardware
            "processor": "Intel(R) Xeon(R) Platinum",
            "number_of_processors": random.choice([1, 2]),
            "number_of_cores": random.choice([8, 16, 32, 64]),
            "ram_gb": random.choice([32, 64, 128, 256, 512]),
            "storage_type": random.choice(["NVMe", "SSD", "SAN"]),
            "storage_capacity_gb": random.choice([500, 1000, 2000, 5000]),
            "storage_used_gb": random.randint(100, 400),

            # Virtualization / Cloud
            "is_virtual": random.choice([True, False]),
            "hypervisor": "VMware ESXi" if i % 2 == 0 else "Hyper-V",
            "cloud_provider": random.choice(["AWS", "Azure", "GCP", None]),
            "instance_id": f"i-{uuid.uuid4().hex[:17]}" if i % 3 == 0 else None,

            # Performance
            "cpu_utilization": random.randint(5, 95),
            "memory_utilization": random.randint(10, 80),
            "disk_utilization": random.randint(20, 90),

            # Services
            "installed_services": "IIS, SQL Server, Monitoring Agent",
            "listening_ports": "80, 443, 1433, 3389",

            # Backup
            "backup_enabled": True,
            "last_backup": timezone.now() - timezone.timedelta(hours=random.randint(1, 24)),

            # Management
            "management_interface": "iDRAC",
            "management_ip": f"10.20.{random.randint(1, 254)}.{random.randint(1, 254)}",

            # Uptime
            "last_boot_time": timezone.now() - timezone.timedelta(days=random.randint(1, 100)),
            "uptime_days": random.randint(1, 100),
        })

        server = Server.objects.create(**data)
        print(f"Server {server.name} ({server.primary_ip_address}) created.")

    print(f"Finished seeding {count} servers.")


if __name__ == "__main__":
    seed_servers(200)