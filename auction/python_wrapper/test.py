from python_wrapper.ipap_field_type import IpapFieldType
from python_wrapper.ipap_field import IpapField
from python_wrapper.ipap_value_field import IpapValueField
from python_wrapper.ipap_field_key import IpapFieldKey
from python_wrapper.ipap_field_container import IpapFieldContainer
from python_wrapper.ipap_data_record import IpapDataRecord
from python_wrapper.ipap_message import IpapMessage

from python_wrapper.ipap_template import IpapTemplate
from python_wrapper.ipap_template import TemplateType
from python_wrapper.ipap_template import UnknownField
from python_wrapper.ipap_template import ObjectType
from python_wrapper.ipap_template_container import IpapTemplateContainerSingleton

from ctypes import pointer
import unittest


class IpapFieldTypeTest(unittest.TestCase):
    """
    IpapFieldTypeTest
    """
    def setUp(self):
        self.ftype = IpapFieldType()

    def test_setters(self):
        self.eno = 10
        self.ftype = 10
        self.length = 10
        self.name = b"casa"
        self.xmlname = b"casa"
        self.documentation = b"casa"

class IpapFieldTest(unittest.TestCase):
    """

    """
    def setUp(self):
        self.ipap_field = IpapField()
        self.ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")
        self.ipap_field2 = IpapField()

    def test_get_eno(self):
        self.assertEqual(self.ipap_field.get_eno(), 0)

    def test_get_type(self):
        self.assertEqual(self.ipap_field.get_type(), 30)

    def test_get_length(self):
        self.assertEqual(self.ipap_field.get_length(), 8)

    def test_get_field_name(self):
        self.assertEqual(self.ipap_field.get_field_name(), b"campo_1")

    def test_get_xml_name(self):
        self.assertEqual(self.ipap_field.get_xml_name(), b"campo_2")

    def test_get_documentation(self):
        self.assertEqual(self.ipap_field.get_documentation(), b"campo_3")

    def test_num_characters(self):
        ipap_field_value = IpapValueField()
        value = b"assd"
        ipap_field_value.set_value_vchar(value, len(value))
        num_characters = self.ipap_field.num_characters(ipap_field_value)
        self.assertEqual(num_characters, 10)

    def test_write_value(self):
        ipap_field_value = IpapValueField()
        value = b"resource_1.set_1"
        size = len(value)
        ipap_field_value.set_value_vchar(value, size)
        self.ipap_field2.set_field_type(0, 30, size, 4, b"campo_1", b"campo_2", b"campo_3")
        result = self.ipap_field2.write_value(ipap_field_value)
        self.assertEqual(result,"resource_1.set_1")



class IpapValueFieldTest(unittest.TestCase):
    """

    """
    def setUp(self):
        self.ipap_field_value = IpapValueField()

    def test_set_value_uint8(self):
        value = 12
        self.ipap_field_value.set_value_uint8(value)
        val = self.ipap_field_value.get_value_uint8()
        self.assertEqual(value, val)

    def test_set_value_uint16(self):
        value = 123
        self.ipap_field_value.set_value_uint16(value)
        val = self.ipap_field_value.get_value_uint16()
        self.assertEqual(value, val)

    def test_set_value_uint32(self):
        value = 213233
        self.ipap_field_value.set_value_uint32(value)
        val = self.ipap_field_value.get_value_uint32()
        self.assertEqual(value, val)

    def test_set_value_uint64(self):
        value = 123187623
        self.ipap_field_value.set_value_uint64(value)
        val = self.ipap_field_value.get_value_uint64()
        self.assertEqual(value, val)

    def test_set_value_float32(self):
        value = 12.46
        self.ipap_field_value.set_value_float32(value)
        val = self.ipap_field_value.get_value_float()
        val = round(val,2)
        self.assertEqual(value, val)

    def test_set_value_double(self):
        value = 12121.45
        self.ipap_field_value.set_value_double(value)
        val = self.ipap_field_value.get_value_double()
        self.assertEqual(value, val)

    def test_set_value_vchar(self):
        value = b"assd"
        self.ipap_field_value.set_value_vchar(value, len(value))
        val = self.ipap_field_value.get_value_vchar()
        self.assertEqual(value, val)


class IpapFieldKeyTest(unittest.TestCase):
    """
    IpapFieldKeyTest
    """
    def setUp(self):
        self.ipap_field_key1 = IpapFieldKey(1, 30)

    def test_get_eno(self):
        val = self.ipap_field_key1.get_eno()
        self.assertEqual(val, 1)

    def test_get_ftype(self):
        val = self.ipap_field_key1.get_ftype()
        self.assertEqual(val, 30)

    def test_get_key(self):
        val = self.ipap_field_key1.get_key()
        self.assertEqual(val, "1-30")


class TemplateTest(unittest.TestCase):

    def setUp(self):
        self.template = IpapTemplate()
        _id = 12
        self.template.set_id(_id)

    def test_set_max_fields(self):
        num_fields = 10
        self.template.set_max_fields(num_fields)

    def test_set_type(self):
        self.template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)

    def test_get_template_type_mandatory_field(self):
        mandatory_fields = self.template.get_template_type_mandatory_field(
                                    TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        # verifies the total number
        self.assertEqual(len(mandatory_fields), 12)

        # verifies that fields returned are correct ones.
        for field in mandatory_fields:
            self.assertEqual(field.get_eno(),0)

    def test_add_field(self):
        ipap_field = IpapField()
        ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")
        self.template.add_field(8, UnknownField.KNOWN, True, ipap_field)

    def test_get_type(self):
        self.template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        template_type = self.template.get_type()
        self.assertEqual(template_type, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)

    def test_get_object_template_types(self):
        with self.assertRaises(ValueError):
            lst = self.template.get_object_template_types(ObjectType.IPAP_INVALID)

        lst = self.template.get_object_template_types(ObjectType.IPAP_AUCTION)
        self.assertEqual(len(lst), 2)

        lst = self.template.get_object_template_types(ObjectType.IPAP_BID)
        self.assertEqual(len(lst), 2)

        lst = self.template.get_object_template_types(ObjectType.IPAP_ALLOCATION)
        self.assertEqual(len(lst), 2)

        lst = self.template.get_object_template_types(ObjectType.IPAP_ASK)
        self.assertEqual(len(lst), 2)


class TemplateContainerTest(unittest.TestCase):

    def setUp(self):
        self.template_container = IpapTemplateContainerSingleton()

    def test_add_template(self):
        ipap_field = IpapField()
        ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")

        _id = 12
        template = IpapTemplate()
        template.set_id(_id)
        template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        template.add_field(8, UnknownField.KNOWN, True, ipap_field)

        self.template_container.add_template(template)

    def test_delete_all_templates(self):
        ipap_field = IpapField()
        ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")

        _id = 12
        template = IpapTemplate()
        template.set_id(_id)
        template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        template.add_field(8, UnknownField.KNOWN, True, ipap_field)

        self.template_container.add_template(template)
        self.template_container.delete_all_templates()
        val = self.template_container.get_num_templates()
        self.assertEqual(val, 0)

    def test_delete_template(self):
        ipap_field = IpapField()
        ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")

        _id = 12
        template = IpapTemplate()
        template.set_id(_id)
        template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        template.add_field(8, UnknownField.KNOWN, True,ipap_field)

        self.template_container.add_template(template)
        self.template_container.delete_template(_id)
        val = self.template_container.get_num_templates()
        self.assertEqual(val, 0)

    def test_exists_template(self):
        ipap_field = IpapField()
        ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")

        _id = 12
        template = IpapTemplate()
        template.set_id(_id)
        template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        template.add_field(8, UnknownField.KNOWN, True, ipap_field)
        self.template_container.add_template(template)

        val = self.template_container.exists_template(_id)
        self.assertEqual(val, True)

        _id = 13
        val = self.template_container.exists_template(_id)
        self.assertEqual(val, False)

    def test_get_template(self):
        ipap_field = IpapField()
        ipap_field.set_field_type(0, 30, 8,  3, b"campo_1", b"campo_2", b"campo_3")

        _id = 12
        template = IpapTemplate()
        template.set_id(_id)
        template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        template.add_field(8, UnknownField.KNOWN, True, ipap_field)
        self.template_container.add_template(template)

        del template

        temp = self.template_container.get_template(_id)
        self.assertEqual(temp.get_template_id(),_id)


class FieldContainerTest(unittest.TestCase):
    """
    FieldContainerTest
    """
    def setUp(self):
        self.field_container = IpapFieldContainer()

    def test_get_field(self):
        self.field_container.initialize_forward()
        field = self.field_container.get_field(0,30)
        self.assertEqual(field.get_field_name(), b"endMilliSeconds")

        with self.assertRaises(ValueError):
            field2 = self.field_container.get_field(0,3000)

    def test_not_initialized(self):
        with self.assertRaises(ValueError):
            field = self.field_container.get_field(0, 30)


class IpapDataRecordTest(unittest.TestCase):
    """
    IpapDataRecordTest
    """
    def setUp(self):

        self.ipap_field_container = IpapFieldContainer()
        self.ipap_field_container.initialize_forward()
        self.ipap_field_container.initialize_reverse()


        self.template = IpapTemplate()
        _id = 2
        self.template.set_id(_id)

        self.ipap_data_record = IpapDataRecord(templ_id=_id)

        self.template.set_type(TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        ipap_field1 = self.ipap_field_container.get_field(0,30)
        ipap_field2 = self.ipap_field_container.get_field(0, 32)

        self.template.add_field(ipap_field1.get_length(), UnknownField.KNOWN, True, ipap_field1)
        self.template.add_field(ipap_field2.get_length(), UnknownField.KNOWN, True, ipap_field2)


    # def test_get_template_id(self):
    #     value = self.ipap_data_record.get_template_id()
    #     self.assertEqual(value,2)
    #
    # def test_insert_field(self):
    #
    #     ipap_field_value1 = IpapValueField()
    #     value = 12
    #     ipap_field_value1.set_value_uint8(value)
    #
    #     ipap_field_value2 = IpapValueField()
    #     value = 13
    #     ipap_field_value2.set_value_uint8(value)
    #
    #     # Replace the value
    #     self.ipap_data_record.insert_field(0, 30, ipap_field_value1)
    #     self.ipap_data_record.insert_field(0, 30, ipap_field_value2)
    #     num_fields = self.ipap_data_record.get_num_fields()
    #     self.assertEqual(num_fields,1)
    #
    #     self.ipap_data_record.insert_field(0, 31, ipap_field_value2)
    #     num_fields = self.ipap_data_record.get_num_fields()
    #     self.assertEqual(num_fields,2)

    def test_get_field(self):


        ipap_field_value1 = IpapValueField()
        value = 12
        ipap_field_value1.set_value_uint8(value)

        # Replace the value
        self.ipap_data_record.insert_field(0, 30, ipap_field_value1)
        num_fields = self.ipap_data_record.get_num_fields()
        self.assertEqual(num_fields,1)

        field = self.ipap_data_record.get_field(0, 30)
        self.assertEqual(field.get_value_uint8(), 12)

        field = self.ipap_field_container.get_field(0, 32)

        value = "record_1"
        # It is required to encode as ascii because the C++ wrapper requires it.
        value_encoded = value.encode('ascii')
        field_val = field.get_ipap_field_value_string(value_encoded)
        self.ipap_data_record.insert_field(0, 32, field_val)

        field = self.template.get_field(0,32)
        output = field.write_value(self.ipap_data_record.get_field( 0, 32))
        print(output)

        num_fields = self.ipap_data_record.get_num_fields()
        self.assertEqual(num_fields,2)

        with self.assertRaises(ValueError):
            field2 = self.ipap_data_record.get_field(0, 33)

    # def test_get_field_length(self):
    #     ipap_field_value1 = IpapValueField()
    #     value = 12
    #     ipap_field_value1.set_value_uint8(value)
    #     # Replace the value
    #     self.ipap_data_record.insert_field(0, 30, ipap_field_value1)
    #     num_fields = self.ipap_data_record.get_num_fields()
    #     self.assertEqual(num_fields,1)
    #
    #     val = self.ipap_data_record.get_field_length(0,30)
    #     self.assertEqual(val, 1)
    #
    # def test_clear(self):
    #     ipap_field_value1 = IpapValueField()
    #     value = 12
    #     ipap_field_value1.set_value_uint8(value)
    #     # Replace the value
    #     self.ipap_data_record.insert_field(0, 30, ipap_field_value1)
    #     num_fields = self.ipap_data_record.get_num_fields()
    #     self.assertEqual(num_fields,1)
    #
    #     self.ipap_data_record.clear()
    #     num_fields = self.ipap_data_record.get_num_fields()
    #     self.assertEqual(num_fields,0)


class IpapMessageTest(unittest.TestCase):
    """
    IpapMessageTest
    """
    def setUp(self):
        self.ipap_message = IpapMessage(1,1,False)
        self.ipap_message2 = IpapMessage(1,1,True)

    def test_new_data_template(self):
        val = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.assertEqual(val, 256)

    def test_add_field(self):
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)

        # test adding an invalid field
        with self.assertRaises(ValueError):
            self.ipap_message.add_field(template_id, 0, 3000)

        # test adding an invalid template id.
        with self.assertRaises(ValueError):
            self.ipap_message.add_field(2, 0, 30)

    def test_delete_template(self):
        print('start test_delete_template')
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)
        self.ipap_message.delete_template(template_id)

        lst = self.ipap_message.get_template_list()
        self.assertEqual(len(lst), 0)

    def test_delete_all_templates(self):
        print('start test_delete_all_templates')
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)
        self.ipap_message.delete_all_templates()
        lst = self.ipap_message.get_template_list()
        self.assertEqual(len(lst), 0)

    def test_get_template_list(self):
        print('start test_get_template_list')
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)
        lst = self.ipap_message.get_template_list()
        self.assertEqual(lst[0], 256)

    def test_get_template_object(self):
        print('start test_get_template_object')
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)

        template = self.ipap_message.get_template_object(template_id)
        template_type = template.get_type()
        self.assertEqual(template_type, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)

        lst = template.get_fields()
        print('num fields:', len(lst))


        with self.assertRaises(ValueError):
            template = self.ipap_message.get_template_object(4)

    def test_include_data(self):
        print('in test_include_data')
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)


        template = self.ipap_message.get_template_object(template_id)
        lst = template.get_fields()

        ipap_data_record = IpapDataRecord(templ_id=template_id)
        ipap_field_value1 = IpapValueField()
        value = 12231213
        ipap_field_value1.set_value_uint64(value)

        template = self.ipap_message.get_template_object(template_id)
        lst = template.get_fields()

        # Replace the value
        ipap_data_record.insert_field(0, 30, ipap_field_value1)
        self.ipap_message.include_data(template_id, ipap_data_record)

        record_size = self.ipap_message.get_data_record_size()
        self.assertEqual(record_size, 1)

    def test_get_data_record_at_pos(self):
        template_id = self.ipap_message.new_data_template(10, TemplateType.IPAP_SETID_AUCTION_TEMPLATE)
        self.ipap_message.add_field(template_id, 0, 30)

        ipap_data_record = IpapDataRecord(templ_id=template_id)
        ipap_field_value1 = IpapValueField()
        value = 12231213
        ipap_field_value1.set_value_uint64(value)

        # Replace the value
        ipap_data_record.insert_field(0, 30, ipap_field_value1)
        self.ipap_message.include_data(template_id, ipap_data_record)
        ipap_data_record2 = self.ipap_message.get_data_record_at_pos(0)

    def test_import(self):
        print('In test import')
        self.ipap_message2.set_syn(True)
        self.ipap_message2.set_seqno(300)
        self.ipap_message2.output()

        str_msg = self.ipap_message2.get_message()
        ipap_message3 = IpapMessage(1,1,True, str_msg)

        str_msg = 'aqui estoy'
        with self.assertRaises(ValueError):
            ipap_message4 = IpapMessage(1, 1, True, str_msg)
