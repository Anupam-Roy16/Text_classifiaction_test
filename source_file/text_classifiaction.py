import re
import telebot
class ExtendedMessage(telebot.types.Message):
    # I want that the original message object is modified having some extra attributes, so need to write the class in that way
    def __init__(self, message):
        # super().__init__()
        self.sanskrit_to_normal_char_map = {
            'ã': 'a', 'ñ': 'n', 'õ': 'o', 'ā': 'a', 'ć': 'c', 'ē': 'e',
            'ĩ': 'i', 'ī': 'i', 'ō': 'o', 'ś': 's', 'ũ': 'u', '।': '।',
            '॥': '॥', '़': 'o', 'ū': 'u', 'ḍ': 'd', 'ḏ': 'd', 'ḥ': 'h',
            'ḷ': 'l', 'ḹ': 'l', 'ḻ': 'l', 'ḿ': 'm', 'ṁ': 'm', 'ṃ': 'm',
            'ṅ': 'n', 'ṇ': 'n', 'ṉ': 'n', 'ṙ': 'r', 'ṛ': 'r', 'ṝ': 'r',
            'ṣ': 's', 'ṥ': 's', 'ṭ': 't', 'ẖ': 'h', 'ẽ': 'e','Ś':'S'
        }
        
        self.message = message
        self.get_fresh_en_quote(message.text)
        self.is_quote = self.is_quote_msg(self.fresh_en_quote)
        self.is_cmd = self.is_cmd_msg(message)
        self.is_warning = self.is_warning_msg(message) 
        self.msg_type = self.determine_msg_type()
    
    def to_normal_text(self,text):
        return ''.join(self.sanskrit_to_normal_char_map.get(char, char) for char in text)

    def get_fresh_en_quote(self,quote_text):
        total_words = re.findall(r'\b\S+\b', quote_text)
        self.fresh_en_quote = ''
        pattern = r'\s*(\S*[ãñõāćēĩīōśũū।॥ḍḏḥḷḹḻḿṁṃṅṇṉṙṛṝṣṥṭẖẽ]+\S*)+\s*'
        for word in total_words:
            word = self.to_normal_text(word)
            self.fresh_en_quote += word + ' '

    def is_quote_msg(self,message_text):
        if re.search(r'S.*Q.*\d+', message_text) and 'Jayapataka' in message_text:
            return True
        else:
            return False

    def is_cmd_msg(self,message):
        return message.text.startswith('/')
    
    def is_warning_msg(self,message):
        return message.text.startswith('WARNING:')
    
    def determine_msg_type(self):
        if self.is_quote:
            return 'quote'
        elif self.is_cmd:
            return 'cmd'
        elif self.is_warning:
            return 'warning'
        else:
            return 'misc'