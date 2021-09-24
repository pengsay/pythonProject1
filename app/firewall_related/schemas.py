from pydantic import BaseModel
from typing import Optional, Any


class AddSecurityRule(BaseModel):
    name: str
    fromzone: Optional[Any] = 'any'
    tozone: Optional[Any] = "any"
    source: Optional[Any] = ""
    source_user: Optional[Any] = ""
    hip_profiles: Optional[Any] = ""
    destination: Optional[Any] = ""
    application: Optional[Any] = ""
    service: Optional[Any] = ""
    category: Optional[Any] = ""
    action: Optional[Any] = ""
    log_setting: Optional[Any] = ""
    log_start: Optional[Any] = ""
    log_end: Optional[bool] = True
    description: Optional[Any] = ""
    type: Optional[Any] = ""
    tag: Optional[Any] = ""
    negate_source: Optional[Any] = ""
    negate_destination: Optional[Any] = ""
    disabled: Optional[Any] = ""
    schedule: Optional[Any] = ""
    icmp_unreachable: Optional[Any] = ""
    disable_server_response_inspection: Optional[Any] = ""
    group: Optional[Any] = ""
    negate_target: Optional[Any] = ""
    target: Optional[Any] = ""
    virus: Optional[Any] = ""
    spyware: Optional[Any] = ""
    vulnerability: Optional[Any] = ""
    url_filtering: Optional[Any] = ""
    file_blocking: Optional[Any] = ""
    wildfire_analysis: Optional[Any] = ""
    data_filtering: Optional[Any] = ""
    uuid: Optional[Any] = ""
    source_devices: Optional[Any] = ""
    destination_devices: Optional[Any] = ""
    group_tag: Optional[Any] = ""


class AddNatRule(BaseModel):
    name: str
    description: Optional[str] = ""
    nat_type: Optional[str] = 'ipv4'
    fromzone: Optional[Any] = 'any'
    tozone: Optional[Any] = "Internal"
    to_interface: Optional[str] = ''
    service: Optional[Any] = ""
    source: Optional[Any] = ""
    destination: Optional[Any] = ""
    source_translation_type: Optional[str] = ''
    source_translation_address_type: Optional[str] = ''
    source_translation_interface: Optional[str] = ''
    source_translation_ip_address: Optional[str] = ''
    source_translation_translated_addresses: Optional[Any] = ''
    source_translation_fallback_type: Optional[str] = ''
    source_translation_fallback_translated_addresses: Optional[Any] = ''
    source_translation_fallback_interface: Optional[str] = ''
    source_translation_fallback_ip_type: Optional[str] = ''
    source_translation_fallback_ip_address: Optional[str] = ''
    source_translation_static_translated_address: Optional[str] = ''
    source_translation_static_bi_directional: Optional[str] = ''
    destination_translated_address: Optional[str] = ''
    destination_translated_port: Optional[str] = ''
    ha_binding: Optional[str] = ''
    disabled: Optional[Any] = ''
    negate_target: Optional[Any] = ''
    target: Optional[Any] = ""
    tag: Optional[Any] = ""
    destination_dynamic_translated_address: Optional[str] = ''
    destination_dynamic_translated_port: Optional[Any] = ''
    destination_dynamic_translated_distribution: Optional[str] = ''
    uuid: Optional[Any] = ""
    group_tag: Optional[Any] = ""
