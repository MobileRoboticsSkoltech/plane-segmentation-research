class FIC:
    @staticmethod
    def compress(input_list_of_integers: list) -> list:
        result = []
        for number in input_list_of_integers:
            temp = []
            if number < (1 << 7):
                temp.append(hex(number))
            elif number < (1 << 14):
                temp.append(hex((number & 0x7F) | 0x80))
                temp.append(hex(number >> 7))
            elif number < (1 << 21):
                temp.append(hex((number & 0x7F) | 0x80))
                temp.append(hex(((number >> 7) & 0x7F) | 0x80))
                temp.append(hex(number >> 14))
            elif number < (1 << 28):
                temp.append(hex((number & 0x7F) | 0x80))
                temp.append(hex(((number >> 7) & 0x7F) | 0x80))
                temp.append(hex(((number >> 14) & 0x7F) | 0x80))
                temp.append(hex(number >> 21))
            else:
                temp.append(hex((number & 0x7F) | 0x80))
                temp.append(hex(((number >> 7) & 0x7F) | 0x80))
                temp.append(hex(((number >> 14) & 0x7F) | 0x80))
                temp.append(hex(((number >> 21) & 0x7F) | 0x80))
                temp.append(hex(number >> 28))

            result.append(temp)

        return result

    @staticmethod
    def decompress(input_byte_array: list) -> list:
        result = []

        for item in input_byte_array:
            temp = 0
            for index, byte in enumerate(item):
                byte_int = (int(byte, 16) & 0x7F) << 7 * index
                temp += byte_int

            result.append(temp)

        return result


class LZW:
    @staticmethod
    def compress(uncompressed: str) -> list:
        dictionary = {}
        word = ""
        result = []
        dict_size = 256

        for i in range(dict_size):
            dictionary[str(chr(i))] = i

        for index in range(len(uncompressed)):
            current_char = str(uncompressed[index])
            word_and_symbol = word + current_char

            if word_and_symbol in dictionary:
                word = word_and_symbol
            else:
                try:
                    result.append(dictionary[word])
                except:
                    print(index)
                    print(word)
                    print("-------------")
                dictionary[word_and_symbol] = dict_size
                dict_size += 1
                word = str(current_char)

        if word != "":
            result.append(dictionary[word])

        return result

    @staticmethod
    def decompress(compressed: list) -> str:
        dictionary = {}
        dict_size = 256

        for i in range(dict_size):
            dictionary[i] = str(chr(i))

        word = str(chr(compressed[0]))
        result = word

        for i in range(1, len(compressed)):
            temp = compressed[i]

            if temp in dictionary:
                entry = dictionary[temp]
            else:
                if temp == dict_size:
                    entry = word + str(word[0])
                else:
                    return 0

            result += entry
            dictionary[dict_size] = word + str(entry[0])
            dict_size += 1
            word = entry

        return result
