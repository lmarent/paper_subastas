from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from foundation.field_value import FieldValue

from typing import Dict
from enum import Enum


class ModuleInformation(Enum):
    I_MODNAME = 0
    I_ID = 0
    I_VERSION = 1
    I_CREATED = 2
    I_MODIFIED = 3
    I_BRIEF = 4
    I_VERBOSE = 5
    I_HTMLDOCS = 6
    I_PARAMS = 7
    I_RESULTS = 8
    I_AUTHOR = 9
    I_AFFILI = 10
    I_EMAIL = 11
    I_HOMEPAGE = 12


class Module(metaclass=ABCMeta):
    """
    this class represents the base class for auction processing modules
    """

    def __init__(self, module_name: str, file_name: str, own_name: str, module_handle):
        self.module_name = module_name
        self.file_name = file_name
        self.own_name = own_name
        self.lib_handle = module_handle
        self.refs = 0
        self.calls = 0

    @abstractmethod
    def init_module(self, config_param_list: Dict[str, FieldValue]):
        """
        Initialization method for starting modules.

        :param config_param_list: Configuration parameters list to
                                   be used on the module.
        """
        pass

    @abstractmethod
    def destroy_module(self):
        """
        Destroy method for ending modules.
        """
        pass

    @abstractmethod
    def execute(self, request_params: Dict[str, FieldValue], auction_key: str, start:datetime, stop:datetime, bids: dict) -> list:
        """
        Executes the module (bidding process)

        :param auction_key: auction key
        :param start: start datetime
        :param stop: stop datetime
        :param bids: bids for the allocation process.
        :return:
        """
        pass

    @abstractmethod
    def execute_user(self, request_params: Dict[str, FieldValue], auctions: dict, start:datetime, stop:datetime) -> list:
        """
        Execute the bidding process for the list of auctions given
        that are required to support a resource request interval.

        :param request_params: parameters given for bidding.
        :param auctions:       auctions that must be executed.
        :param start:          start datetime
        :param stop:           stop datetime

        :return: bids created by the auction process.
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset flow data record for a rule

        :return:
        """
        pass

    def set_own_name(self, own_name:str):
        """
        Sets own name
        :param own_name: own name
        """
        self.own_name=own_name

    def link(self):
        """
        increases module reference counter
        """
        self.refs = self.refs + 1

    def unlink(self):
        """
        decreases module reference counter
        """
        self.refs = self.refs - 1

    def get_module_handle(self):
        """
        Gets the module handle
        :return:
        """
        return self.lib_handle

    def get_module_name(self) -> str:
        """
        Gets module name
        :return:
        """
        return self.module_name

    def get_file_name(self) -> str:
        """
        Gets the file name from where the module was loaded
        :return:
        """
        return self.file_name

    def get_own_name(self) -> str:
        """
        Gets the own name
        :return:
        """
        return self.own_name

    def get_references(self) -> int:
        """
        Gets teh reference count
        :return:
        """
        return self.refs
