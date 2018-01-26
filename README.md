# Json definition

## Aggregates

List all aggregates 

### Aggregates route

```
get /4.0/ontap/aggregates 
```

### Aggregates key

```json
{
    "aggregate_type": "hdd",
    "block_type": "64_bit",
    "cluster_key": "9667888e-a18d-11e4-b631-00a09879d036:type=cluster,uuid=9667888e-a18d-11e4-b631-00a09879d036",
    "has_local_root": false,
    "has_partner_root": false,
    "hybrid_cache_size_total": 0,
    "is_hybrid": false,
    "is_hybrid_enabled": false,
    "is_snaplock": false,
    "key": "9667888e-a18d-11e4-b631-00a09879d036:type=aggregate,uuid=c9bfe695-a4d7-4c8b-9de5-d318b84df8f2",
    "mirror_status": "unmirrored",
    "name": "A_CABU_01_SATA",
    "node_key": "9667888e-a18d-11e4-b631-00a09879d036:type=cluster_node,uuid=6e70b674-a024-11e4-b3c6-a9ba0c1a3109",
    "raid_size": 14,
    "raid_status": "raid_dp, normal",
    "raid_type": "raid_dp",
    "size_avail": 8492258914304,
    "size_avail_percent": 79,
    "size_total": 10780462161920,
    "size_used": 2288203247616,
    "size_used_percent": 21,
    "snaplock_type": "non_snaplock",
    "snapshot_size_avail": 0,
    "snapshot_size_total": 0,
    "snapshot_size_used": 0,
    "state": "online",
    "total_committed": 2275258925056,
    "total_reserved_space": 0,
    "uses_shared_disks": false,
    "volume_compression_space_savings": 0,
    "volume_dedupe_space_savings": 0
}
```

## Volumes

get volume from aggregates 

### Volume route

```
KEY = key from aggregates
get /4.0/ontap/aggregates/{key}/volumes 
```

### Volumes key
```json
{
    "aggregate_keys": [
        "9667888e-a18d-11e4-b631-00a09879d036:type=aggregate,uuid=4f3fca90-b76c-4c4f-8447-b066b91fb061"
    ],
    "auto_size_increment_size": 53686272,
    "auto_size_maximum_size": 1288273920,
    "auto_size_mode": "off",
    "clone_parent_key": null,
    "compression_space_saved": 0,
    "deduplication_space_saved": 0,
    "derived_style": "flexvol",
    "export_policy_key": "9667888e-a18d-11e4-b631-00a09879d036:type=export_policy,uuid=51539607553",
    "flex_cache_min_reserve": null,
    "flex_cache_origin_key": null,
    "hybrid_cache_eligibility": "read_write",
    "inode_block_type": "64_bit",
    "inode_files_total": 31122,
    "inode_files_used": 99,
    "instance_uuid": "89f9f913-c9a3-498c-9eb8-9f06eceffdd3",
    "is_atime_update_enabled": true,
    "is_auto_snapshots_enabled": false,
    "is_convert_ucode_enabled": true,
    "is_create_ucode_enabled": true,
    "is_data_compaction_enabled": null,
    "is_data_protection_mirror": false,
    "is_encryption_enabled": null,
    "is_i2p_enabled": true,
    "is_junction_active": true,
    "is_load_sharing_mirror": false,
    "is_move_mirror": false,
    "is_replica_volume": false,
    "is_sis_compression_enabled": null,
    "is_sis_inline_compression_enabled": null,
    "is_sis_inline_dedupe_enabled": null,
    "is_sis_volume": false,
    "is_snap_dir_access_enabled": true,
    "is_snapshot_auto_delete_enabled": false,
    "is_snapshot_clone_dependency_enabled": false,
    "is_space_guarantee_enabled": true,
    "is_storage_vm_root": false,
    "junction_parent_key": "9667888e-a18d-11e4-b631-00a09879d036:type=volume,uuid=1eb2b020-39fd-46dc-9368-5ebed6a1514d",
    "junction_path": "/v_red_htd_log",
    "key": "9667888e-a18d-11e4-b631-00a09879d036:type=volume,uuid=89f9f913-c9a3-498c-9eb8-9f06eceffdd3",
    "language_code": "fr",
    "name": "v_red_htd_log",
    "oldest_snapshot_timestamp": null,
    "overwrite_reserve": 0,
    "overwrite_reserve_actual_used": 0,
    "overwrite_reserve_avail": 0,
    "overwrite_reserve_required": 0,
    "overwrite_reserve_used": 0,
    "percentage_compression_space_saved": 0,
    "percentage_deduplication_space_saved": 0,
    "percentage_fractional_reserve": 100,
    "percentage_snapshot_reserve": 0,
    "percentage_snapshot_reserve_used": 0,
    "qos_policy_group_key": null,
    "quota_committed": 0,
    "quota_over_committed": 0,
    "quota_status": "off",
    "read_realloc": null,
    "scheduled_snapshot_name": null,
    "security_group_id": "501",
    "security_permissions": "755",
    "security_style": "unix",
    "security_user_id": "501",
    "sis_last_op_begin_timestamp": null,
    "sis_last_op_end_timestamp": null,
    "sis_last_op_error": null,
    "sis_last_op_size": null,
    "sis_last_op_state": null,
    "sis_policy_key": null,
    "sis_progress": null,
    "sis_schedule": null,
    "sis_state": null,
    "sis_status": null,
    "sis_type": null,
    "size": 1073741824,
    "size_avail": 897060864,
    "size_avail_percent": 84,
    "size_available_for_snapshot": 897060864,
    "f": 1073741824,
    "size_used": 176680960,
    "size_used_by_snapshots": 14458880,
    "size_used_percent": 16,
    "snapshot_auto_delete_commitment": "try",
    "snapshot_auto_delete_defer_delete": "user_created",
    "snapshot_auto_delete_delete_order": "oldest_first",
    "snapshot_auto_delete_destroy_list": "none",
    "snapshot_auto_delete_prefix": "(not specified)",
    "snapshot_auto_delete_target_free_space": 20,
    "snapshot_auto_delete_trigger": "volume",
    "snapshot_policy_key": "9667888e-a18d-11e4-b631-00a09879d036:type=snapshot_policy,vserver_uuid=a046a5b0-a18d-11e4-b631-00a09879d036,name=none",
    "snapshot_reserve_size": 0,
    "space_guarantee": "volume",
    "space_mgmt_option_try_first": "volume_grow",
    "state": "online",
    "storage_vm_key": "9667888e-a18d-11e4-b631-00a09879d036:type=vserver,uuid=b27392ac-e990-11e4-be25-00a09879d036",
    "style": "flex",
    "vm_align_sector": null,
    "vm_align_suffix": null,
    "vol_type": "rw"
}
```

## Nodes

### Node route 

```
get /4.0/ontap/nodes
```

### Nodes Key

```json
    {
        "cpu_processor_type": "Intel(R) Xeon(R) CPU           C3528  @ 1.73GHz",
        "model": "FAS2552",
        "location": "SALLE VERTE",
        "memory_size": 19327352832,
        "is_node_healthy": true,
        "interconnect_links": "RDMA Interconnect is up (Link up)",
        "takeover_by_partner_not_possible_reason": null,
        "version": "NetApp Release 9.1P8: Wed Aug 30 13:33:41 UTC 2017",
        "local_firmware_state": "SF_UP",
        "name": "CABU-01",
        "version_major": 1,
        "partner_firmware_state": "SF_UP",
        "key": "9667888e-a18d-11e4-b631-00a09879d036:type=cluster_node,uuid=6e70b674-a024-11e4-b3c6-a9ba0c1a3109",
        "nvram_id": "536911092",
        "takeover_failure_reason": null,
        "version_generation": 9,
        "is_interconnect_up": true,
        "interconnect_type": "Infiniband (Mellanox Sinai)",
        "metro_cluster_dr_partner_node_key": null,
        "is_over_temperature": false,
        "failed_fan_count": 0,
        "cluster_key": "9667888e-a18d-11e4-b631-00a09879d036:type=cluster,uuid=9667888e-a18d-11e4-b631-00a09879d036",
        "vendor": "NetApp",
        "current_mode": "ha",
        "is_failover_enabled": true,
        "metro_cluster_dr_operation_state": null,
        "env_failed_fan_message": "There are no failed fans.",
        "uptime": 5953732,
        "takeover_of_partner_not_possible_reason": null,
        "is_take_over_possible": true,
        "product_type": "FAS",
        "failed_power_supply_count": 0,
        "cpu_firmware_release": "8.3.0",
        "nvram_battery_status": "battery_ok",
        "partner_node_key": "9667888e-a18d-11e4-b631-00a09879d036:type=cluster_node,uuid=57d56984-a03c-11e4-ade2-43d2570c109e",
        "is_epsilon_node": false,
        "serial_number": "651443000131",
        "give_back_state": "nothing_to_gb",
        "version_minor": 0,
        "env_failed_power_supply_message": "There are no failed power supplies.",
        "cpu_processor_id": "0x106e4",
        "owner": null,
        "is_all_flash_optimized": false,
        "failover_state": "connected",
        "number_of_processors": 4
    }
```

