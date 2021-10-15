class FIC:
    @staticmethod
    def compress(input_list_of_integers: list) -> list:
        result = []
        for number in input_list_of_integers:
            if number < (1 << 7):
                result.append(hex(number))
            elif number < (1 << 14):
                result.append(hex((number & 0x7F) | 0x80))
                result.append(hex(number >> 7))
            elif number < (1 << 21):
                result.append(hex((number & 0x7F) | 0x80))
                result.append(hex(((number >> 7) & 0x7F) | 0x80))
                result.append(hex(number >> 14))
            elif number < (1 << 28):
                result.append(hex((number & 0x7F) | 0x80))
                result.append(hex(((number >> 7) & 0x7F) | 0x80))
                result.append(hex(((number >> 14) & 0x7F) | 0x80))
                result.append(hex(number >> 21))
            else:
                result.append(hex((number & 0x7F) | 0x80))
                result.append(hex(((number >> 7) & 0x7F) | 0x80))
                result.append(hex(((number >> 14) & 0x7F) | 0x80))
                result.append(hex(((number >> 21) & 0x7F) | 0x80))
                result.append(hex(number >> 28))

        return result

    @staticmethod
    def decompress(input_byte_array: list) -> list:
        size = len(input_byte_array)
        position = 0
        result = []

        while size > position:
            byte = int(input_byte_array[position], 16)
            position += 1
            temp = byte & 0x7F
            if byte >= 0:
                result.append(temp)
                continue
            byte = input_byte_array[position]
            position += 1
            temp |= (byte & 0x7F) << 7
            if byte >= 0:
                print("Hi!")
                result.append(int(temp, 16))
                continue
            byte = input_byte_array[position]
            position += 1
            temp |= (byte & 0x7F) << 14
            if byte >= 0:
                result.append(temp)
                continue
            byte = input_byte_array[position]
            position += 1
            temp |= (byte & 0x7F) << 21
            if byte >= 0:
                result.append(temp)
                continue
            byte = input_byte_array[position]
            position += 1
            temp |= byte << 28
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
