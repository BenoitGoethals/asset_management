from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import uuid


class BaseAsset(models.Model):
    """Abstract base model for all asset types with common attributes"""

    # Status choices
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        MAINTENANCE = 'MAINTENANCE', 'Under Maintenance'
        RETIRED = 'RETIRED', 'Retired'
        LOST = 'LOST', 'Lost/Stolen'
        DISPOSED = 'DISPOSED', 'Disposed'

    class Environment(models.TextChoices):
        PRODUCTION = 'PROD', 'Production'
        STAGING = 'STAG', 'Staging'
        DEVELOPMENT = 'DEV', 'Development'
        TESTING = 'TEST', 'Testing'
        DISASTER_RECOVERY = 'DR', 'Disaster Recovery'

    class RiskLevel(models.TextChoices):
        CRITICAL = 'CRITICAL', 'Critical'
        HIGH = 'HIGH', 'High'
        MEDIUM = 'MEDIUM', 'Medium'
        LOW = 'LOW', 'Low'

    # Unique identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_tag = models.CharField(max_length=100, unique=True, help_text="Unique asset identification tag")
    serial_number = models.CharField(max_length=200, blank=True, null=True, help_text="Manufacturer serial number")

    # Basic information
    name = models.CharField(max_length=255, help_text="Human-readable asset name")
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    model = models.CharField(max_length=200, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)

    # Network information
    hostname = models.CharField(max_length=255, blank=True, null=True)
    fqdn = models.CharField(max_length=500, blank=True, null=True, help_text="Fully Qualified Domain Name")
    primary_ip_address = models.GenericIPAddressField(blank=True, null=True)
    secondary_ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True, null=True, help_text="Primary MAC address")
    subnet_mask = models.GenericIPAddressField(blank=True, null=True)
    default_gateway = models.GenericIPAddressField(blank=True, null=True)
    dns_servers = models.TextField(blank=True, null=True, help_text="Comma-separated DNS servers")
    vlan_id = models.IntegerField(blank=True, null=True, help_text="VLAN identifier")

    # Location information
    physical_location = models.CharField(max_length=500, blank=True, null=True)
    building = models.CharField(max_length=200, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)
    room = models.CharField(max_length=100, blank=True, null=True)
    rack_location = models.CharField(max_length=100, blank=True, null=True)
    rack_unit = models.CharField(max_length=50, blank=True, null=True)
    geographic_location = models.CharField(max_length=300, blank=True, null=True, help_text="City, State, Country")
    site = models.CharField(max_length=200, blank=True, null=True, help_text="Site or campus identifier")

    # Organizational information
    department = models.CharField(max_length=200, blank=True, null=True)
    cost_center = models.CharField(max_length=100, blank=True, null=True)
    business_unit = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='owned_%(class)s_assets')
    custodian = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='custodian_%(class)s_assets',
                                  help_text="Person responsible for day-to-day management")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_%(class)s_assets')

    # Lifecycle information
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    warranty_expiration = models.DateField(blank=True, null=True)
    support_expiration = models.DateField(blank=True, null=True)
    lease_expiration = models.DateField(blank=True, null=True)
    end_of_life_date = models.DateField(blank=True, null=True)
    disposal_date = models.DateField(blank=True, null=True)
    vendor = models.CharField(max_length=200, blank=True, null=True)
    purchase_order = models.CharField(max_length=100, blank=True, null=True)

    # Status and compliance
    status = models.CharField(max_length=20, choices=Status, default=Status.ACTIVE)
    environment = models.CharField(max_length=10, choices=Environment, default=Environment.PRODUCTION)
    risk_level = models.CharField(max_length=10, choices=RiskLevel, default=RiskLevel.MEDIUM)
    compliance_status = models.BooleanField(default=True, help_text="Is asset compliant with security policies")
    authorized = models.BooleanField(default=True, help_text="Is this an authorized asset")
    managed = models.BooleanField(default=True, help_text="Is this asset actively managed")

    # Discovery and monitoring
    first_discovered = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(blank=True, null=True, help_text="Last time asset was detected on network")
    last_scanned = models.DateTimeField(blank=True, null=True, help_text="Last security/inventory scan")
    discovery_method = models.CharField(max_length=100, blank=True, null=True,
                                        help_text="How was this asset discovered")
    monitoring_enabled = models.BooleanField(default=True)

    # Security attributes
    encrypted = models.BooleanField(default=False, help_text="Disk encryption enabled")
    encryption_method = models.CharField(max_length=100, blank=True, null=True)
    antivirus_installed = models.BooleanField(default=False)
    antivirus_version = models.CharField(max_length=100, blank=True, null=True)
    antivirus_last_update = models.DateTimeField(blank=True, null=True)
    firewall_enabled = models.BooleanField(default=False)
    patch_level = models.CharField(max_length=200, blank=True, null=True)
    last_patched = models.DateTimeField(blank=True, null=True)
    vulnerability_score = models.IntegerField(blank=True, null=True,
                                              validators=[MinValueValidator(0), MaxValueValidator(10)])

    # Additional metadata
    notes = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")
    configuration_items = models.JSONField(blank=True, null=True, help_text="Additional configuration data")

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_%(class)s_assets')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='updated_%(class)s_assets')

    class Meta:
        abstract = True
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'authorized']),
            models.Index(fields=['primary_ip_address']),
            models.Index(fields=['hostname']),
        ]

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"


class EndUserDevice(BaseAsset):
    """Model for end-user devices: desktops, laptops, tablets, mobile devices"""

    class DeviceType(models.TextChoices):
        DESKTOP = 'DESKTOP', 'Desktop Computer'
        LAPTOP = 'LAPTOP', 'Laptop'
        TABLET = 'TABLET', 'Tablet'
        SMARTPHONE = 'SMARTPHONE', 'Smartphone'
        THIN_CLIENT = 'THIN_CLIENT', 'Thin Client'
        WORKSTATION = 'WORKSTATION', 'Workstation'

    class OperatingSystem(models.TextChoices):
        WINDOWS_11 = 'WIN11', 'Windows 11'
        WINDOWS_10 = 'WIN10', 'Windows 10'
        MACOS = 'MACOS', 'macOS'
        LINUX = 'LINUX', 'Linux'
        IOS = 'IOS', 'iOS'
        ANDROID = 'ANDROID', 'Android'
        CHROME_OS = 'CHROMEOS', 'Chrome OS'

    # Device specific information
    device_type = models.CharField(max_length=20, choices=DeviceType)
    operating_system = models.CharField(max_length=20, choices=OperatingSystem)
    os_version = models.CharField(max_length=100, blank=True, null=True)
    os_build = models.CharField(max_length=100, blank=True, null=True)
    os_architecture = models.CharField(max_length=20, blank=True, null=True, help_text="32-bit or 64-bit")

    # Hardware specifications
    processor = models.CharField(max_length=200, blank=True, null=True)
    processor_speed = models.CharField(max_length=50, blank=True, null=True)
    number_of_cores = models.IntegerField(blank=True, null=True)
    ram_gb = models.IntegerField(blank=True, null=True, help_text="RAM in GB")
    storage_type = models.CharField(max_length=50, blank=True, null=True, help_text="HDD, SSD, NVMe")
    storage_capacity_gb = models.IntegerField(blank=True, null=True)
    storage_used_gb = models.IntegerField(blank=True, null=True)
    graphics_card = models.CharField(max_length=200, blank=True, null=True)
    display_size = models.CharField(max_length=50, blank=True, null=True)
    display_resolution = models.CharField(max_length=50, blank=True, null=True)

    # Mobile specific
    imei = models.CharField(max_length=17, blank=True, null=True, help_text="International Mobile Equipment Identity")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    carrier = models.CharField(max_length=100, blank=True, null=True)
    sim_card_number = models.CharField(max_length=100, blank=True, null=True)

    # Management
    domain_joined = models.BooleanField(default=False)
    domain_name = models.CharField(max_length=200, blank=True, null=True)
    mdm_enrolled = models.BooleanField(default=False, help_text="Mobile Device Management enrollment")
    mdm_platform = models.CharField(max_length=100, blank=True, null=True)
    remote_wipe_enabled = models.BooleanField(default=False)

    # Software and applications
    installed_software = models.TextField(blank=True, null=True, help_text="List of installed applications")
    licensed_software = models.TextField(blank=True, null=True)

    # Usage
    primary_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='primary_devices')
    last_login = models.DateTimeField(blank=True, null=True)
    last_boot_time = models.DateTimeField(blank=True, null=True)
    uptime_hours = models.IntegerField(blank=True, null=True)

    # Battery (for mobile devices)
    battery_health = models.IntegerField(blank=True, null=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(100)])
    battery_cycle_count = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "End User Device"
        verbose_name_plural = "End User Devices"
        indexes = [
            models.Index(fields=['device_type', 'operating_system']),
            models.Index(fields=['imei']),
        ]


class NetworkDevice(BaseAsset):
    """Model for network infrastructure devices"""

    class DeviceType(models.TextChoices):
        ROUTER = 'ROUTER', 'Router'
        SWITCH = 'SWITCH', 'Switch'
        FIREWALL = 'FIREWALL', 'Firewall'
        LOAD_BALANCER = 'LB', 'Load Balancer'
        ACCESS_POINT = 'AP', 'Wireless Access Point'
        WIRELESS_CONTROLLER = 'WLC', 'Wireless Controller'
        VPN_CONCENTRATOR = 'VPN', 'VPN Concentrator'
        IDS_IPS = 'IDS_IPS', 'IDS/IPS'
        PROXY = 'PROXY', 'Proxy Server'
        DNS_SERVER = 'DNS', 'DNS Server'
        DHCP_SERVER = 'DHCP', 'DHCP Server'
        NAS = 'NAS', 'Network Attached Storage'

    # Device specific
    device_type = models.CharField(max_length=20, choices=DeviceType)
    firmware_version = models.CharField(max_length=100, blank=True, null=True)
    ios_version = models.CharField(max_length=100, blank=True, null=True, help_text="For Cisco devices")

    # Network specifications
    number_of_ports = models.IntegerField(blank=True, null=True)
    port_speed = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 1Gbps, 10Gbps")
    poe_enabled = models.BooleanField(default=False, help_text="Power over Ethernet")
    poe_budget_watts = models.IntegerField(blank=True, null=True)

    # Capacity and performance
    throughput_mbps = models.IntegerField(blank=True, null=True, help_text="Maximum throughput in Mbps")
    max_connections = models.IntegerField(blank=True, null=True)
    current_connections = models.IntegerField(blank=True, null=True)
    cpu_utilization = models.IntegerField(blank=True, null=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    memory_utilization = models.IntegerField(blank=True, null=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Redundancy
    redundant_power_supply = models.BooleanField(default=False)
    high_availability_enabled = models.BooleanField(default=False)
    failover_partner = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='failover_devices')

    # Management
    management_ip = models.GenericIPAddressField(blank=True, null=True)
    management_interface = models.CharField(max_length=100, blank=True, null=True)
    snmp_enabled = models.BooleanField(default=False)
    snmp_community = models.CharField(max_length=200, blank=True, null=True)
    ssh_enabled = models.BooleanField(default=True)
    telnet_enabled = models.BooleanField(default=False)
    https_enabled = models.BooleanField(default=True)

    # Configuration
    configuration_backup = models.TextField(blank=True, null=True)
    last_config_backup = models.DateTimeField(blank=True, null=True)
    config_compliance = models.BooleanField(default=True)

    # Uplink and connectivity
    uplink_device = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='downlink_devices')
    connected_vlans = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated VLAN IDs")

    # Wireless specific (for APs and controllers)
    wifi_standard = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 802.11ax (WiFi 6)")
    ssid_list = models.TextField(blank=True, null=True, help_text="List of SSIDs")
    max_clients = models.IntegerField(blank=True, null=True)
    current_clients = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Network Device"
        verbose_name_plural = "Network Devices"
        indexes = [
            models.Index(fields=['device_type', 'status']),
            models.Index(fields=['management_ip']),
        ]


class IoTDevice(BaseAsset):
    """Model for Internet of Things devices"""

    class DeviceType(models.TextChoices):
        IP_CAMERA = 'CAMERA', 'IP Camera'
        SENSOR = 'SENSOR', 'Sensor'
        ACCESS_CONTROL = 'ACCESS', 'Access Control System'
        HVAC = 'HVAC', 'HVAC Controller'
        LIGHTING = 'LIGHTING', 'Smart Lighting'
        PRINTER = 'PRINTER', 'Network Printer'
        BADGE_READER = 'BADGE', 'Badge Reader'
        ENVIRONMENTAL = 'ENVIRONMENTAL', 'Environmental Monitor'
        INDUSTRIAL = 'INDUSTRIAL', 'Industrial Control'
        SMART_DISPLAY = 'DISPLAY', 'Smart Display'
        OTHER = 'OTHER', 'Other IoT Device'

    # Device specific
    device_type = models.CharField(max_length=20, choices=DeviceType)
    firmware_version = models.CharField(max_length=100, blank=True, null=True)

    # Technical specifications
    protocol = models.CharField(max_length=100, blank=True, null=True,
                                help_text="Communication protocol (MQTT, Modbus, etc.)")
    power_source = models.CharField(max_length=100, blank=True, null=True, help_text="Battery, PoE, AC")
    wireless_type = models.CharField(max_length=50, blank=True, null=True, help_text="WiFi, Bluetooth, Zigbee, etc.")

    # Camera specific
    camera_resolution = models.CharField(max_length=50, blank=True, null=True)
    camera_type = models.CharField(max_length=50, blank=True, null=True, help_text="PTZ, Fixed, Dome")
    recording_enabled = models.BooleanField(default=False)
    recording_location = models.CharField(max_length=300, blank=True, null=True)

    # Sensor specific
    sensor_type = models.CharField(max_length=100, blank=True, null=True,
                                   help_text="Temperature, Humidity, Motion, etc.")
    measurement_unit = models.CharField(max_length=50, blank=True, null=True)
    current_reading = models.CharField(max_length=100, blank=True, null=True)
    last_reading_time = models.DateTimeField(blank=True, null=True)
    alert_threshold = models.CharField(max_length=100, blank=True, null=True)

    # Access control specific
    reader_type = models.CharField(max_length=100, blank=True, null=True, help_text="RFID, Biometric, PIN")
    access_level = models.CharField(max_length=100, blank=True, null=True)

    # Printer specific
    printer_type = models.CharField(max_length=50, blank=True, null=True, help_text="Laser, Inkjet, MFP")
    print_server = models.CharField(max_length=200, blank=True, null=True)
    supplies_status = models.CharField(max_length=200, blank=True, null=True)
    page_count = models.IntegerField(blank=True, null=True)

    # Management and security
    default_password_changed = models.BooleanField(default=False, help_text="Has default password been changed")
    remote_access_enabled = models.BooleanField(default=False)
    internet_accessible = models.BooleanField(default=False, help_text="Directly accessible from internet")
    segmented_network = models.BooleanField(default=False, help_text="On isolated/segmented network")

    # Lifecycle
    last_reboot = models.DateTimeField(blank=True, null=True)
    uptime_days = models.IntegerField(blank=True, null=True)

    # Integration
    cloud_service = models.CharField(max_length=200, blank=True, null=True, help_text="Connected cloud service")
    api_enabled = models.BooleanField(default=False)
    integration_platform = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "IoT Device"
        verbose_name_plural = "IoT Devices"
        indexes = [
            models.Index(fields=['device_type', 'status']),
            models.Index(fields=['internet_accessible']),
        ]


class Server(BaseAsset):
    """Model for physical, virtual, and cloud servers"""

    class ServerType(models.TextChoices):
        PHYSICAL = 'PHYSICAL', 'Physical Server'
        VIRTUAL = 'VIRTUAL', 'Virtual Machine'
        CLOUD = 'CLOUD', 'Cloud Instance'
        CONTAINER = 'CONTAINER', 'Container'

    class OperatingSystem(models.TextChoices):
        WINDOWS_SERVER_2022 = 'WIN2022', 'Windows Server 2022'
        WINDOWS_SERVER_2019 = 'WIN2019', 'Windows Server 2019'
        RHEL = 'RHEL', 'Red Hat Enterprise Linux'
        UBUNTU = 'UBUNTU', 'Ubuntu Server'
        CENTOS = 'CENTOS', 'CentOS'
        DEBIAN = 'DEBIAN', 'Debian'
        SUSE = 'SUSE', 'SUSE Linux'
        VMWARE_ESXI = 'ESXI', 'VMware ESXi'
        OTHER = 'OTHER', 'Other'

    class ServerRole(models.TextChoices):
        WEB_SERVER = 'WEB', 'Web Server'
        DATABASE = 'DB', 'Database Server'
        APPLICATION = 'APP', 'Application Server'
        FILE_SERVER = 'FILE', 'File Server'
        MAIL_SERVER = 'MAIL', 'Mail Server'
        DNS = 'DNS', 'DNS Server'
        DHCP = 'DHCP', 'DHCP Server'
        DOMAIN_CONTROLLER = 'DC', 'Domain Controller'
        HYPERVISOR = 'HYPERVISOR', 'Hypervisor'
        BACKUP = 'BACKUP', 'Backup Server'
        MONITORING = 'MONITORING', 'Monitoring Server'
        PROXY = 'PROXY', 'Proxy Server'
        OTHER = 'OTHER', 'Other'

    # Server specific
    server_type = models.CharField(max_length=20, choices=ServerType)
    operating_system = models.CharField(max_length=20, choices=OperatingSystem)
    os_version = models.CharField(max_length=100, blank=True, null=True)
    os_edition = models.CharField(max_length=100, blank=True, null=True)
    kernel_version = models.CharField(max_length=100, blank=True, null=True)
    server_role = models.CharField(max_length=20, choices=ServerRole)

    # Hardware/Virtual specifications
    processor = models.CharField(max_length=200, blank=True, null=True)
    number_of_processors = models.IntegerField(blank=True, null=True)
    number_of_cores = models.IntegerField(blank=True, null=True)
    ram_gb = models.IntegerField(blank=True, null=True)
    storage_type = models.CharField(max_length=100, blank=True, null=True, help_text="Local, SAN, NFS, etc.")
    storage_capacity_gb = models.IntegerField(blank=True, null=True)
    storage_used_gb = models.IntegerField(blank=True, null=True)

    # Virtualization
    is_virtual = models.BooleanField(default=False)
    hypervisor = models.CharField(max_length=100, blank=True, null=True)
    hypervisor_host = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='virtual_machines')
    vm_id = models.CharField(max_length=100, blank=True, null=True)
    vm_tools_version = models.CharField(max_length=100, blank=True, null=True)

    # Cloud specific
    cloud_provider = models.CharField(max_length=100, blank=True, null=True, help_text="AWS, Azure, GCP, etc.")
    cloud_region = models.CharField(max_length=100, blank=True, null=True)
    cloud_availability_zone = models.CharField(max_length=100, blank=True, null=True)
    instance_type = models.CharField(max_length=100, blank=True, null=True)
    instance_id = models.CharField(max_length=200, blank=True, null=True)
    cloud_account_id = models.CharField(max_length=200, blank=True, null=True)

    # Performance
    cpu_utilization = models.IntegerField(blank=True, null=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    memory_utilization = models.IntegerField(blank=True, null=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    disk_utilization = models.IntegerField(blank=True, null=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    network_throughput_mbps = models.IntegerField(blank=True, null=True)

    # Services and applications
    installed_services = models.TextField(blank=True, null=True)
    listening_ports = models.TextField(blank=True, null=True, help_text="Comma-separated port numbers")
    running_processes = models.TextField(blank=True, null=True)

    # Database specific (if database server)
    database_type = models.CharField(max_length=100, blank=True, null=True, help_text="MySQL, PostgreSQL, Oracle, etc.")
    database_version = models.CharField(max_length=100, blank=True, null=True)
    database_size_gb = models.IntegerField(blank=True, null=True)
    databases_hosted = models.TextField(blank=True, null=True)

    # Web server specific
    web_server_software = models.CharField(max_length=100, blank=True, null=True, help_text="Apache, Nginx, IIS")
    web_server_version = models.CharField(max_length=100, blank=True, null=True)
    hosted_websites = models.TextField(blank=True, null=True)
    ssl_certificate_expiration = models.DateField(blank=True, null=True)

    # Backup and disaster recovery
    backup_enabled = models.BooleanField(default=False)
    backup_schedule = models.CharField(max_length=200, blank=True, null=True)
    last_backup = models.DateTimeField(blank=True, null=True)
    backup_location = models.CharField(max_length=300, blank=True, null=True)
    disaster_recovery_plan = models.BooleanField(default=False)
    rto_hours = models.IntegerField(blank=True, null=True, help_text="Recovery Time Objective in hours")
    rpo_hours = models.IntegerField(blank=True, null=True, help_text="Recovery Point Objective in hours")

    # High availability
    clustered = models.BooleanField(default=False)
    cluster_name = models.CharField(max_length=200, blank=True, null=True)
    cluster_nodes = models.TextField(blank=True, null=True)
    load_balanced = models.BooleanField(default=False)

    # Management
    management_interface = models.CharField(max_length=200, blank=True, null=True, help_text="iDRAC, iLO, IPMI")
    management_ip = models.GenericIPAddressField(blank=True, null=True)
    remote_management_enabled = models.BooleanField(default=False)

    # Compliance and licensing
    licensed = models.BooleanField(default=True)
    license_key = models.CharField(max_length=300, blank=True, null=True)
    license_expiration = models.DateField(blank=True, null=True)
    license_count = models.IntegerField(blank=True, null=True)

    # Monitoring and logging
    monitoring_agent_installed = models.BooleanField(default=False)
    monitoring_agent_version = models.CharField(max_length=100, blank=True, null=True)
    log_forwarding_enabled = models.BooleanField(default=False)
    syslog_server = models.CharField(max_length=200, blank=True, null=True)

    # Uptime
    last_boot_time = models.DateTimeField(blank=True, null=True)
    uptime_days = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"
        indexes = [
            models.Index(fields=['server_type', 'operating_system']),
            models.Index(fields=['server_role', 'environment']),
            models.Index(fields=['cloud_provider', 'instance_id']),
        ]


class AssetChangeLog(models.Model):
    """Track all changes made to assets for audit purposes"""

    asset_type = models.CharField(max_length=100)
    asset_id = models.UUIDField()
    asset_name = models.CharField(max_length=255)
    change_type = models.CharField(max_length=50, help_text="Created, Updated, Deleted")
    changed_fields = models.JSONField(help_text="Dictionary of changed fields and their old/new values")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Asset Change Log"
        verbose_name_plural = "Asset Change Logs"
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['asset_type', 'asset_id']),
            models.Index(fields=['changed_at']),
        ]

    def __str__(self):
        return f"{self.change_type} - {self.asset_name} at {self.changed_at}"