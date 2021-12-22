class FIC:
    @staticmethod
    def compress(input_list_of_integers: list) -> list:
        result = []
        for number in input_list_of_integers:
            if number < (1 << 7):
                result.append((number).to_bytes(1, byteorder="little"))
            elif number < (1 << 14):
                result.append(((number & 0x7F) | 0x80).to_bytes(1, byteorder="little"))
                result.append((number >> 7).to_bytes(1, byteorder="little"))
            elif number < (1 << 21):
                result.append(((number & 0x7F) | 0x80).to_bytes(1, byteorder="little"))
                result.append((((number >> 7) & 0x7F) | 0x80)).to_bytes(
                    1, byteorder="little"
                )
                result.append((number >> 14).to_bytes(1, byteorder="little"))
            elif number < (1 << 28):
                result.append(((number & 0x7F) | 0x80).to_bytes(1, byteorder="little"))
                result.append((((number >> 7) & 0x7F) | 0x80)).to_bytes(
                    1, byteorder="little"
                )
                result.append((((number >> 14) & 0x7F) | 0x80)).to_bytes(
                    1, byteorder="little"
                )
                result.append((number >> 21).to_bytes(1, byteorder="little"))
            else:
                result.append(((number & 0x7F) | 0x80).to_bytes(1, byteorder="little"))
                result.append((((number >> 7) & 0x7F) | 0x80)).to_bytes(
                    1, byteorder="little"
                )
                result.append((((number >> 14) & 0x7F) | 0x80)).to_bytes(
                    1, byteorder="little"
                )
                result.append((((number >> 21) & 0x7F) | 0x80)).to_bytes(
                    1, byteorder="little"
                )
                result.append((number >> 28).to_bytes(1, byteorder="little"))

        return result

    @staticmethod
    def decompress(input_byte_array: list) -> list:
        result = []
        position = 0

        while len(input_byte_array) > position:
            byte_to_int = int.from_bytes(
                input_byte_array[position], signed=True, byteorder="little"
            )
            position += 1
            temp_int = byte_to_int & 0x7F
            if byte_to_int >= 0:
                result.append(temp_int)
                continue
            byte_to_int = int.from_bytes(
                input_byte_array[position], signed=True, byteorder="little"
            )
            position += 1
            temp_int |= (byte_to_int & 0x7F) << 7
            if byte_to_int >= 0:
                result.append(temp_int)
                continue
            byte_to_int = int.from_bytes(
                input_byte_array[position], signed=True, byteorder="little"
            )
            position += 1
            temp_int |= (byte_to_int & 0x7F) << 14
            if byte_to_int >= 0:
                result.append(temp_int)
                continue
            byte_to_int = int.from_bytes(
                input_byte_array[position], signed=True, byteorder="little"
            )
            position += 1
            temp_int |= (byte_to_int & 0x7F) << 21
            if byte_to_int >= 0:
                result.append(temp_int)
                continue
            byte_to_int = int.from_bytes(
                input_byte_array[position], signed=True, byteorder="little"
            )
            position += 1
            temp_int |= byte_to_int << 28
            result.append(temp_int)

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
