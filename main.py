import string

class DbBase64:

    base64_chars_table = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

    def __init__(self) -> None:
        self._number_of_padding = 0
        self.debug = False
    
    def _convert_ascii_to_decimal(self, data: str) -> list[int]:
        """
        Conversion of ASCII characters from str to the list with decimal values.

        :param data: String to conversion.
        :type data: str
        :return: List of converted values.
        :rtype: list[int]
        """
        result = []
        for character in data:
            result.append(ord(character))
        if self.debug == True:
            print(data)
            print(type(result))
            print(result)
        return result

    def _convert_to_8_bit_number(self, data: list[int]) -> list[str]:
        """
        Conversion of decimal values to binary values.

        :param data: list of decimal values
        :type data: list[int]
        :return: List of binary values as a strings.
        :rtype: list[str]
        """
        result = []
        sup_data = []
        for ascii_char in data:
            sup_data.append(bin(ascii_char)[2:])
        for element in sup_data:
            rest = 8 - (len(element) % 8)
            zerro_to_add = rest * '0'
            element = zerro_to_add + element
            result.append(element)
        if self.debug == True:
            print(result)
        return result

    def _div_into_6_bit_block(self, data: list[str]) -> list[str]:
        """
        Conversion of 8 bit blocks to 6 bit blocks.
        in: ['01001101', '01100001', '01101110']
        out: ['010011', '010110', '000101', '101110']
        more info: https://en.wikipedia.org/wiki/Base64

        :param data: List of binary values as a strings.
        :type data: list[str]
        :return: List of binary values as a strings.
        :rtype: list[str]
        """
        result = []
        concatenated_string = ''
        block_6_bit = ''

        for element in data:
            concatenated_string += element
        for single_bit in concatenated_string:
            block_6_bit += single_bit
            if len(block_6_bit) == 6:
                result.append(block_6_bit)
                block_6_bit = ''
        if len(block_6_bit) != 0:
            result.append(f"{block_6_bit}{(6 - len(block_6_bit)) * '0'}")
        
        if (len(result) % 4):
            self._number_of_padding = 4 - (len(result) % 4)

        if self.debug == True:
            print(f'Number of padding: {self._number_of_padding}')
            print(result)

        return result

    def _convert_to_int(self, data: list[str]) -> list[int]:
        """
        Conversion of 6 bit blocks to decimal values.
        Example 
        in: ['010011', '010110', '000100']
        out: [19, 22, 4]

        :param data: List of binary values as a strings.
        :type data: list[str]
        :return: List of decimal values.
        :rtype: list[int]
        """
        result = []
        converted_digit = 0
        for element in data:
            converted_digit = int(f'0b{element}', 2)
            result.append(converted_digit)

        if self.debug == True:
            print(result)

        return result

    def _map_int_to_base64_table(self, data: list[int]) -> list[str]:
        """
        Mapping decimal values to base64 table values.
        Example
        in: [19, 22, 4]
        out: ['T', 'W', 'E', '=']

        :param data: List of decimal values.
        :type data: list[str]
        :return: List of base64 characters.
        :rtype: list[int]
        """
        result = []
        char_base64 = None
        for digit in data:
            char_base64 = self.base64_chars_table[digit]
            result.append(char_base64)
        for _ in range(self._number_of_padding):
            result.append('=')

        if self.debug == True:
            print(result)

        return result
    
    def ascii_to_base64(self, data: str) -> str:
        """
        Encodes an ASCII string into base64 form.
        Example
        in: 'Ma'
        out: 'TWE='

        :param data: String to conversion.
        :type data: str
        :return: Coded string (base64).
        :rtype: str
        """
        if not isinstance(data, str):
            error = f' Argument  data must be of type str. type(data) -> {type(data)}'
            raise TypeError(error)
        if not data.isascii():
            error = f'data = {data}. String must consist of ASCII characters only.'
            raise TypeError(error)
        data = self._convert_ascii_to_decimal(data)
        data = self._convert_to_8_bit_number(data)
        data = self._div_into_6_bit_block(data)
        data = self._convert_to_int(data)
        data = self._map_int_to_base64_table(data)
        return ''.join(data)
        



def main():

    data_set = [
        'Man',
        'Ma',
        'M',
        'Nowa praca ',
        'ąćę',
        5
    ]

    db_base64 = DbBase64()
    db_base64.debug = True

    
    for ascii_string in data_set:
        try:
            print(db_base64.ascii_to_base64(ascii_string))
            print('---------------------------------')
        except TypeError as e:
            print('Błąd TypeError:', str(e))

main()
