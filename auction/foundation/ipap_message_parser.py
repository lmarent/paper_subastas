from python_wrapper.ipap_template import IpapTemplate, ObjectType, TemplateType
from python_wrapper.ipap_message import IpapMessage
from python_wrapper.ipap_data_record import IpapDataRecord
from python_wrapper.ipap_field import IpapField
from python_wrapper.ipap_field_container import IpapFieldContainer

from foundation.field_def_manager import FieldDefManager
from foundation.config_param import ConfigParam
from datetime import datetime


class IpapMessageParser:

    def __init__(self, domain: int):
        self.domain = domain
        self.field_def_manager = FieldDefManager()
        self.field_container = IpapFieldContainer()
        self.field_container.initialize_reverse()
        self.field_container.initialize_forward()

    @staticmethod
    def parse_name(id_auction: str) -> (str, str):
        """
        Parses an object name (auction or bid).

        :param id_auction: Identifier formated as 'setname.objectname'
        :return: (set_name, name)
        """
        if len(id_auction) == 0:
            raise ValueError("malformed identifier {0}, use <identifier> or <set>.<identifier> ".format(id_auction))

        ids = id_auction.split(".")

        if len(ids) == 0:
            raise ValueError("malformed identifier {0}, use <identifier> or <set>.<identifier> ".format(id_auction))

        elif len(ids) == 1:
            set_name = ""
            name = ids[0]
            return set_name, name

        elif len(ids) == 2:
            set_name = ids[0]
            name = ids[1]
            return set_name, name
        else:
            raise ValueError("malformed identifier {0}, use <identifier> or <set>.<identifier> ".format(id_auction))

    @staticmethod
    def parse_object_type(s_type: str) -> ObjectType:
        """
        Parses the type of bidding object

        :param s_type: object type represented as string
        :return:
        """
        if (s_type == "auction") or (s_type == "0"):
            obj_type = ObjectType.IPAP_AUCTION
            return obj_type

        elif (s_type == "bid") or (s_type == "1"):
            obj_type = ObjectType.IPAP_BID
            return obj_type

        elif (s_type == "ask") or (s_type == "2"):
            obj_type = ObjectType.IPAP_ASK
            return obj_type

        elif (s_type == "allocation") or (s_type == "3"):
            obj_type = ObjectType.IPAP_ALLOCATION
            return obj_type

        else:
            raise ValueError("Bidding Object Parser Error: invalid bidding object type {0}".format(s_type))

    @staticmethod
    def parse_template_type(obj_type: ObjectType, templ_type: str) -> TemplateType:
        """
        Parses a template type

        :param obj_type: object type for which this template type belongs to
        :param templ_type: template type represented as string
        :return: template type
        """
        if obj_type == ObjectType.IPAP_AUCTION:
            if templ_type == "data":
                return TemplateType.IPAP_SETID_AUCTION_TEMPLATE
            elif templ_type == "option":
                return TemplateType.IPAP_OPTNS_AUCTION_TEMPLATE

        elif obj_type == ObjectType.IPAP_BID:
            if templ_type == "data":
                return TemplateType.IPAP_SETID_BID_OBJECT_TEMPLATE
            elif templ_type == "option":
                return TemplateType.IPAP_OPTNS_BID_OBJECT_TEMPLATE

        elif obj_type == ObjectType.IPAP_ASK:
            if templ_type == "data":
                return TemplateType.IPAP_SETID_ASK_OBJECT_TEMPLATE
            elif templ_type == "option":
                return TemplateType.IPAP_OPTNS_ASK_OBJECT_TEMPLATE

        elif obj_type == ObjectType.IPAP_ALLOCATION:
            if templ_type == "data":
                return TemplateType.IPAP_SETID_ALLOC_OBJECT_TEMPLATE
            elif templ_type == "option":
                return TemplateType.IPAP_OPTNS_ALLOC_OBJECT_TEMPLATE

        raise ValueError("Bidding Object Parser Error: invalid template type")

    @staticmethod
    def read_template(message: IpapMessage, template_type: TemplateType) -> IpapTemplate:
        """
        Reads a template type from a message.

        :return: Ipap Template
        """
        temp_list = message.get_template_list()
        for id_template in temp_list:
            template = message.get_template_object(id_template)
            if template.get_type() == template_type:
                return template

        raise ValueError("Template not found")

    @staticmethod
    def read_data_records(message: IpapMessage, templ_id: int) -> list:
        """
        Reads the data record list from a message

        templ_id : template identifier.
        :return: list of data records within the message.
        """
        size = message.get_data_record_size()
        list_return = []
        for i in range(0, size):
            data_record = message.get_data_record_at_pos(i)
            if data_record.get_template_id() == templ_id:
                list_return.append(data_record)
        return list_return

    def get_domain(self) -> int:
        """
        Get the domaid id used by the ipapmessage.The domain id corresponds to the agent identifier.
        :return: domain
        """
        return self.domain

    def get_misc_val(self, config_items: dict, item_name: str):

        if item_name in config_items:
            item: ConfigParam = config_items[item_name]
            value = item.value.lower()
            return value
        else:
            raise ValueError("item with name {0} not found in config items".format(item_name))

    def insert_string_field(self, field_name: str, value: str, record: IpapDataRecord):
        """
        Inserts a field value in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        field_def = self.field_def_manager.get_field(field_name)
        field: IpapField = self.field_container.get_field(
            int(field_def['eno']), int(field_def['ftype']))
        record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                            field.get_ipap_field_value_string(value))

    def insert_integer_field(self, field_name: str, value: int, record: IpapDataRecord):
        """
        Inserts a field value in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        field_def = self.field_def_manager.get_field(field_name)
        field: IpapField = self.field_container.get_field(
            int(field_def['eno']), int(field_def['ftype']))

        if field.get_length() == 1:
            record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                                field.get_ipap_field_value_uint8(value))
        elif field.get_length() == 2:
            record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                                field.get_ipap_field_value_uint16(value))
        elif field.get_length() == 4:
            record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                                field.get_ipap_field_value_uint32(value))
        elif field.get_length() == 8:
            record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                                field.get_ipap_field_value_uint64(value))

    def insert_float_field(self, field_name: str, value: float, record: IpapDataRecord):
        """
        Inserts a field value in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        field_def = self.field_def_manager.get_field(field_name)
        field: IpapField = self.field_container.get_field(
            int(field_def['eno']), int(field_def['ftype']))
        record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                            field.get_ipap_field_value_float(value))

    def insert_double_field(self, field_name: str, value: float, record: IpapDataRecord):
        """
        Inserts a field value (double) in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        field_def = self.field_def_manager.get_field(field_name)
        field: IpapField = self.field_container.get_field(
            int(field_def['eno']), int(field_def['ftype']))
        record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                            field.get_ipap_field_value_double(value))

    def insert_ipv4_field(self, field_name: str, value: str, record: IpapDataRecord):
        """
        Inserts a field value (ip address 4) in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        field_def = self.field_def_manager.get_field(field_name)
        field: IpapField = self.field_container.get_field(
            int(field_def['eno']), int(field_def['ftype']))
        record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                            field.get_ipap_field_value_ipv4(value))

    def insert_ipv6_field(self, field_name: str, value: str, record: IpapDataRecord):
        """
        Inserts a field value (ip address 6) in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        field_def = self.field_def_manager.get_field(field_name)
        field: IpapField = self.field_container.get_field(
            int(field_def['eno']), int(field_def['ftype']))
        record.insert_field(int(field_def['eno']), int(field_def['ftype']),
                            field.get_ipap_field_value_ipv6(value))

    def insert_datetime_field(self, field_name: str, value: datetime, record: IpapDataRecord):
        """
        Inserts a field value (datetime) in the data record given as parameter

        :param field_name: field to be inserted
        :param value: value to insert
        :param record: data record where the field is going to be inserted.
        """
        seconds = int((value - datetime.fromtimestamp(0)).total_seconds())
        self.insert_integer_field(field_name, seconds, record)
