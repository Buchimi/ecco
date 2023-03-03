from enum import Enum
from typing import Union

from ..utils import BeanieInternalTypeError


class LLVMValueType(Enum):
    """Enum class that stores LLVM values"""

    NONE = "LLVMValue (None)"

    VIRTUAL_REGISTER = "LLVMVALUE (Virtual Register)"

    def __str__(self) -> str:
        return self.value

    def __int__(self) -> int:
        return LLVMValueType._member_names_.index(self._name_)


class LLVMValue:
    def __init__(self, lvt: LLVMValueType, value: Union[int, None]):
        """Stores data about various kinds of LLVM Values

        Args:
            lvt (LLVMValueType): The type of LLVMValue to instantiate
            value (Union[int, None]): The stored value

        Raises:
            BeanieInternalTypeError: _description_
        """
        self.value_type: LLVMValueType = lvt
        if self.value_type == LLVMValueType.VIRTUAL_REGISTER:
            if type(value) != int:
                raise BeanieInternalTypeError(str(int), str(type(value)),
                                              "generation/llvmvalue.py:LLVMValue.__init__",)
            self.int_value: int = value
    
    def __repr__(self) -> str:
        append: str = ""
        if self.value_type == LLVMValueType.VIRTUAL_REGISTER:
            append = f": %{self.int_value}"
        return f"LLVMValue ({self.value_type})" + append
