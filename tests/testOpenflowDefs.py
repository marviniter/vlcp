'''
Created on 2015/7/20/

:author: hubo
'''
from __future__ import print_function
import unittest
from vlcp.protocol.openflow import common, openflow10, openflow13
from vlcp.utils.namedstruct import nstruct, dump
from pprint import pprint

class Test(unittest.TestCase):
    exclude = [common.ofp_error_experimenter_msg, openflow13.ofp_group_desc_stats, openflow13.ofp_oxm_mask, openflow13.ofp_oxm_nomask, openflow13._ofp_oxm_mask_value,
               openflow13.ofp_action_set_field, openflow10.nx_flow_mod_spec, openflow13.nx_flow_mod_spec, openflow10.nx_matches, openflow13.nx_matches]
    def testDefs10(self):
        for k in dir(openflow10):
            attr = getattr(openflow10, k)
            if isinstance(attr, nstruct) and not attr in self.exclude and not k.startswith('nxm_'):
                if not attr.subclasses:
                    self.assertEqual(k, repr(attr), k + ' has different name: ' + repr(attr))
                    print(k, repr(attr))
                    obj = attr.new()
                    s = obj._tobytes()
                    r = attr.parse(s)
                    self.assertTrue(r is not None, repr(attr) + ' failed to parse')
                    obj2, size = r
                    self.assertEqual(size, len(s), repr(attr) + ' failed to parse')
                    self.assertEqual(dump(obj), dump(obj2), repr(attr) + ' changed after parsing')
    def testDefs13(self):
        for k in dir(openflow13):
            attr = getattr(openflow13, k)
            if isinstance(attr, nstruct) and not attr in self.exclude and not k.startswith('ofp_oxm_') and not k.startswith('nxm_'):
                if not attr.subclasses:
                    self.assertEqual(k, repr(attr), k + ' has different name: ' + repr(attr))
                    print(k, repr(attr))
                    obj = attr.new()
                    s = obj._tobytes()
                    r = attr.parse(s)
                    self.assertTrue(r is not None, repr(attr) + ' failed to parse')
                    obj2, size = r
                    self.assertEqual(size, len(s), repr(attr) + ' failed to parse')
                    self.assertEqual(dump(obj), dump(obj2), repr(attr) + ' changed after parsing')
    def testOxm(self):
        fm = openflow13.ofp_flow_mod.new(priority = openflow13.OFP_DEFAULT_PRIORITY, command = openflow13.OFPFC_ADD, buffer_id = openflow13.OFP_NO_BUFFER)
        fm.cookie = 0x67843512
        fm.match = openflow13.ofp_match_oxm.new()
        fm.match.oxm_fields.append(openflow13.create_oxm(openflow13.OXM_OF_ETH_DST, b'\x06\x00\x0c\x15\x45\x99'))
        fm.match.oxm_fields.append(openflow13.create_oxm(openflow13.OXM_OF_ETH_TYPE, common.ETHERTYPE_IP))
        fm.match.oxm_fields.append(openflow13.create_oxm(openflow13.OXM_OF_IP_PROTO, 6))
        fm.match.oxm_fields.append(openflow13.create_oxm(openflow13.OXM_OF_IPV4_SRC_W, [192,168,1,0], [255,255,255,0]))
        apply = openflow13.ofp_instruction_actions.new(type = openflow13.OFPIT_APPLY_ACTIONS)
        apply.actions.append(openflow13.ofp_action_set_field.new(field = openflow13.create_oxm(openflow13.OXM_OF_IPV4_SRC, [202, 102, 0, 37])))
        apply.actions.append(openflow13.ofp_action_set_queue.new(queue_id = 1))
        fm.instructions.append(apply)
        write = openflow13.ofp_instruction_actions.new(type = openflow13.OFPIT_WRITE_ACTIONS)
        write.actions.append(openflow13.ofp_action_output.new(port = 7))
        fm.instructions.append(write)
        goto = openflow13.ofp_instruction_goto_table.new(table_id = 1)
        fm.instructions.append(goto)
        s = fm._tobytes()
        r = common.ofp_msg.parse(s)
        self.assertTrue(r is not None, 'Cannot parse message')
        obj2, size = r
        self.assertEqual(size, len(s), 'Cannot parse message')
        pprint(dump(fm))
        pprint(dump(obj2))
        self.assertEqual(dump(fm), dump(obj2), 'message changed after parsing')
    def testDefs13Size(self):
        # From openflow.h
        self.assertEqual(len(openflow13.ofp_header()),8)
        self.assertEqual(openflow13.ofp_hello_elem()._realsize(),4)        # Excluding padding
        self.assertEqual(openflow13.ofp_hello_elem_versionbitmap()._realsize(),4)
        self.assertEqual(len(openflow13.ofp_hello()),8)
        self.assertEqual(len(openflow13.ofp_switch_config()),12)
        self.assertEqual(len(openflow13.ofp_table_mod()),16)
        self.assertEqual(len(openflow13.ofp_port()),64)
        self.assertEqual(len(openflow13.ofp_switch_features()),32)
        self.assertEqual(len(openflow13.ofp_port_status()),80)
        self.assertEqual(len(openflow13.ofp_port_mod()),40)
        self.assertEqual(len(openflow13.ofp_match()),8)
        self.assertEqual(len(openflow13.ofp_oxm_experimenter()),8)
        self.assertEqual(len(openflow13.ofp_action()),8)
        self.assertEqual(len(openflow13.ofp_action_output()),16)
        self.assertEqual(len(openflow13.ofp_action_mpls_ttl()),8)
        self.assertEqual(len(openflow13.ofp_action_push()),8)
        self.assertEqual(len(openflow13.ofp_action_pop_mpls()),8)
        self.assertEqual(len(openflow13.ofp_action_group()),8)
        self.assertEqual(len(openflow13.ofp_action_nw_ttl()),8)
        self.assertEqual(len(openflow13.ofp_action_set_field()),8)
        self.assertEqual(len(openflow13.ofp_action_experimenter()),8)
        self.assertEqual(openflow13.ofp_instruction()._realsize(),4)
        self.assertEqual(len(openflow13.ofp_instruction_goto_table()),8)
        self.assertEqual(len(openflow13.ofp_instruction_write_metadata()),24)
        self.assertEqual(len(openflow13.ofp_instruction_actions()),8)
        self.assertEqual(len(openflow13.ofp_instruction_meter()),8)
        self.assertEqual(len(openflow13.ofp_instruction_experimenter()),8)
        self.assertEqual(len(openflow13.ofp_flow_mod()),56)
        self.assertEqual(len(openflow13.ofp_bucket()),16)
        self.assertEqual(len(openflow13.ofp_group_mod()),16)
        self.assertEqual(len(openflow13.ofp_packet_out()),24)
        self.assertEqual(len(openflow13.ofp_packet_in()),34)    # Add the extra padding
        self.assertEqual(len(openflow13.ofp_flow_removed()),56)
        self.assertEqual(openflow13.ofp_meter_band()._realsize(),12)
        self.assertEqual(len(openflow13.ofp_meter_band_drop()),16)
        self.assertEqual(len(openflow13.ofp_meter_band_dscp_remark()),16)
        self.assertEqual(len(openflow13.ofp_meter_band_experimenter()),16)
        self.assertEqual(len(openflow13.ofp_meter_mod()),16)
        self.assertEqual(len(openflow13.ofp_error_msg()),12)
        self.assertEqual(len(openflow13.ofp_error_experimenter_msg()),16)
        self.assertEqual(len(openflow13.ofp_multipart_request()),16)
        self.assertEqual(len(openflow13.ofp_multipart_reply()),16)
        self.assertEqual(len(openflow13.ofp_desc()),1056)
        self.assertEqual(len(openflow13.ofp_flow_stats_request()),40 + len(openflow13.ofp_multipart_request()))
        self.assertEqual(len(openflow13.ofp_flow_stats()),56)
        self.assertEqual(len(openflow13.ofp_aggregate_stats_request()),40 + len(openflow13.ofp_multipart_request()))
        self.assertEqual(len(openflow13.ofp_aggregate_stats_reply()),24 + len(openflow13.ofp_multipart_reply()))
        self.assertEqual(openflow13.ofp_table_feature_prop()._realsize(),4)
        self.assertEqual(openflow13.ofp_table_feature_prop_instructions()._realsize(),4)
        self.assertEqual(openflow13.ofp_table_feature_prop_next_tables()._realsize(),4)
        self.assertEqual(openflow13.ofp_table_feature_prop_actions()._realsize(),4)
        self.assertEqual(openflow13.ofp_table_feature_prop_oxm()._realsize(),4)
        self.assertEqual(openflow13.ofp_table_feature_prop_experimenter()._realsize(),12)
        self.assertEqual(len(openflow13.ofp_table_features()),64)
        self.assertEqual(len(openflow13.ofp_table_stats()),24)
        self.assertEqual(len(openflow13.ofp_port_stats_request()),8 + len(openflow13.ofp_multipart_request()))
        self.assertEqual(len(openflow13.ofp_port_stats()),112)
        self.assertEqual(len(openflow13.ofp_group_stats_request()),8 + len(openflow13.ofp_multipart_request()))
        self.assertEqual(len(openflow13.ofp_bucket_counter()),16)
        self.assertEqual(len(openflow13.ofp_group_stats()),40)
        self.assertEqual(len(openflow13.ofp_group_desc()),8)
        self.assertEqual(len(openflow13.ofp_group_features()),40)
        self.assertEqual(len(openflow13.ofp_meter_multipart_request()),8 + len(openflow13.ofp_multipart_request()))
        self.assertEqual(len(openflow13.ofp_meter_band_stats()),16)
        self.assertEqual(len(openflow13.ofp_meter_stats()),40)
        self.assertEqual(len(openflow13.ofp_meter_config()),8 + len(openflow13.ofp_multipart_reply()))
        self.assertEqual(len(openflow13.ofp_meter_features()),16)
        self.assertEqual(len(openflow13.ofp_experimenter_multipart_header()),8)
        self.assertEqual(len(openflow13.ofp_experimenter()),16)
        self.assertEqual(len(openflow13.ofp_queue_prop_header()),8)
        self.assertEqual(len(openflow13.ofp_queue_prop_min_rate()),16)
        self.assertEqual(len(openflow13.ofp_queue_prop_max_rate()),16)
        self.assertEqual(len(openflow13.ofp_queue_prop_experimenter()),16)
        self.assertEqual(len(openflow13.ofp_packet_queue()),16)
        self.assertEqual(len(openflow13.ofp_queue_get_config_request()),16)
        self.assertEqual(len(openflow13.ofp_queue_get_config_reply()),16)
        self.assertEqual(len(openflow13.ofp_action_set_queue()),8)
        self.assertEqual(len(openflow13.ofp_queue_stats_request()),8 + len(openflow13.ofp_multipart_reply()))
        self.assertEqual(len(openflow13.ofp_queue_stats()),40)
        self.assertEqual(len(openflow13.ofp_role_request()),24)
        self.assertEqual(len(openflow13.ofp_async_config()),32)
    def testDefs10Size(self):
        self.assertEqual(len(openflow10.ofp_header()),8)
        self.assertEqual(len(openflow10.ofp_phy_port()),48)
        self.assertEqual(len(openflow10.ofp_packet_queue()),8)
        self.assertEqual(len(openflow10.ofp_queue_prop_header()),8)
        self.assertEqual(len(openflow10.ofp_queue_prop_min_rate()),16)
        self.assertEqual(len(openflow10.ofp_match()),40)
        self.assertEqual(len(openflow10.ofp_action()),8)
        self.assertEqual(len(openflow10.ofp_action_output()),8)
        self.assertEqual(len(openflow10.ofp_action_enqueue()),16)
        self.assertEqual(len(openflow10.ofp_action_vlan_vid()),8)
        self.assertEqual(len(openflow10.ofp_action_vlan_pcp()),8)
        self.assertEqual(len(openflow10.ofp_action_dl_addr()),16)
        self.assertEqual(len(openflow10.ofp_action_nw_addr()),8)
        self.assertEqual(len(openflow10.ofp_action_nw_tos()),8)
        self.assertEqual(len(openflow10.ofp_action_tp_port()),8)
        self.assertEqual(len(openflow10.ofp_action_vendor()),8)
        self.assertEqual(len(openflow10.ofp_switch_features()),32)
        self.assertEqual(len(openflow10.ofp_switch_config()),12)
        self.assertEqual(len(openflow10.ofp_flow_mod()),72)
        self.assertEqual(len(openflow10.ofp_port_mod()),32)
        self.assertEqual(len(openflow10.ofp_queue_get_config_request()),12)
        self.assertEqual(len(openflow10.ofp_queue_get_config_reply()),16)
        self.assertEqual(len(openflow10.ofp_stats_request()),12)
        self.assertEqual(len(openflow10.ofp_stats_reply()),12)
        self.assertEqual(len(openflow10.ofp_desc_stats()),1056)
        self.assertEqual(len(openflow10.ofp_flow_stats_request()),44 + len(openflow10.ofp_stats_request()))
        self.assertEqual(len(openflow10.ofp_flow_stats()),88)
        self.assertEqual(len(openflow10.ofp_aggregate_stats_request()),44 + len(openflow10.ofp_stats_request()))
        self.assertEqual(len(openflow10.ofp_aggregate_stats_reply()),24 + len(openflow10.ofp_stats_reply()))
        self.assertEqual(len(openflow10.ofp_table_stats()),64)
        self.assertEqual(len(openflow10.ofp_port_stats_request()),8 + len(openflow10.ofp_stats_request()))
        self.assertEqual(len(openflow10.ofp_port_stats()),104)
        self.assertEqual(len(openflow10.ofp_queue_stats_request()),8 + len(openflow10.ofp_stats_request()))
        self.assertEqual(len(openflow10.ofp_queue_stats()),32)
        self.assertEqual(len(openflow10.ofp_packet_out()),16)
        self.assertEqual(len(openflow10.ofp_packet_in()),18)        # No extra padding
        self.assertEqual(len(openflow10.ofp_flow_removed()),88)
        self.assertEqual(len(openflow10.ofp_port_status()),64)
        self.assertEqual(len(openflow10.ofp_error_msg()),12)
        self.assertEqual(len(openflow10.ofp_vendor()),12)
    def testDefs10ExtSize(self):
        self.assertEqual(len(openflow10.nicira_header()),16)
        self.assertEqual(len(openflow10.nx_stats_request()),24)
        self.assertEqual(len(openflow10.nx_flow_mod_table_id()),8 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_set_packet_in_format()),4 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_packet_in()),24 + len(openflow10.nicira_header()) + 2) # Extra padding
        self.assertEqual(len(openflow10.nx_role_request()),4 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_async_config()),24 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_set_flow_format()),4 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_flow_mod()),32 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_flow_removed()),40 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_flow_stats_request()),8 + len(openflow10.nx_stats_request()))
        self.assertEqual(len(openflow10.nx_flow_stats()),48)
        self.assertEqual(len(openflow10.nx_aggregate_stats_request()),8 + len(openflow10.nx_stats_request()))
        self.assertEqual(len(openflow10.nx_controller_id()),8 + len(openflow10.nicira_header()))
        self.assertEqual(len(openflow10.nx_flow_monitor_request()),16 + len(openflow10.nx_stats_request()))
        self.assertEqual(openflow10.nx_flow_update()._realsize(),4)
        self.assertEqual(len(openflow10.nx_flow_update_full()),24)
        self.assertEqual(len(openflow10.nx_flow_update_abbrev()),8)
        self.assertEqual(len(openflow10.nx_flow_monitor_cancel()),4 + len(openflow10.nicira_header()))
    def testDefs13ExtSize(self):
        self.assertEqual(len(openflow13.nicira_header()),16)
        self.assertEqual(len(openflow13.nx_stats_request()),24)
        self.assertEqual(len(openflow13.nx_flow_mod_table_id()),8 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_set_packet_in_format()),4 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_packet_in()),24 + len(openflow13.nicira_header()) + 2) # Extra padding
        self.assertEqual(len(openflow13.nx_role_request()),4 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_async_config()),24 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_set_flow_format()),4 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_flow_mod()),32 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_flow_removed()),40 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_flow_stats_request()),8 + len(openflow13.nx_stats_request()))
        self.assertEqual(len(openflow13.nx_flow_stats()),48)
        self.assertEqual(len(openflow13.nx_aggregate_stats_request()),8 + len(openflow13.nx_stats_request()))
        self.assertEqual(len(openflow13.nx_controller_id()),8 + len(openflow13.nicira_header()))
        self.assertEqual(len(openflow13.nx_flow_monitor_request()),16 + len(openflow13.nx_stats_request()))
        self.assertEqual(openflow13.nx_flow_update()._realsize(),4)
        self.assertEqual(len(openflow13.nx_flow_update_full()),24)
        self.assertEqual(len(openflow13.nx_flow_update_abbrev()),8)
        self.assertEqual(len(openflow13.nx_flow_monitor_cancel()),4 + len(openflow13.nicira_header()))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDefs']
    unittest.main()