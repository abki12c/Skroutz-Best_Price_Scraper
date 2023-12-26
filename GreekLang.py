import re
from collections import OrderedDict

class GreekLang:

    @staticmethod
    def toGreeklish(text):
        # Conversion is based on ELOT 743

        GR = list("ΑΆΒΓΔΕΈΖΗΉΙΊΪΚΛΜΝΞΟΌΠΡΣΤΥΎΫΦΩΏαάβγδεέζηήιίϊΐκλμνξοόπρσςτυύϋΰφωώ")
        EN = list("AAVGDEEZIIIIIKLMNXOOPRSTYYYFOOaavgdeeziiiiiiklmnxooprsstyyyyfoo")

        translation_dictionary = dict()

        for i in range (len(GR)):
                translation_dictionary[GR[i]] = EN[i]

        syllables = [
                     ['γχ','nch'],['αυ(?=[θκξπστφχψ])','af'],['ευ(?=[θκξπστφχψ|\s|$])','ef'], ['εύ(?=[θκξπστφχψ|\s|$])','ef'],
                     ['ηυ(?=[θκξπστφχψ|\s|$])','if'],['(?=^|\s|$)μπ','b'],['μπ(?=^|\s|$)','b'],
                     ['αι','ai'],['οι','oi'],['ου','ou'],['ού','ou'],['ει','ei'],['ντ','nt'],['τσ','ts'],
                     ['τζ','tz'],['γγ','ng'],['γκ','gk'],['θ','th'],['χ','x'],['ψ','ps'],
                     ['αυ','av'],['ευ','ev'],['ηυ','if'],['μπ','mp'],
                     ['Γχ', 'Nch'],['Αυ(?=[θκξπστφχψ])','Af'],['Ευ(?=[θκξπστφχψ|\s|$])','Ef'], ['Εύ(?=[θκξπστφχψ|\s|$])','Ef'],
                     ['Ηυ(?=[θκξπστφχψ|\s|$])','If'],['(?=^|\s|$)Μπ','B'],['Μπ(?=^|\s|$)','B'],
                     ['Αι','Ai'],['Οι','Oi'],['Ου','Ou'],['Ού', 'Ou'],['Ει','Ei'],['Ντ','Nt'],['Τς','Ts'],
                     ['Τζ','Tz'],['Γγ','Ng'],['Γκ','Gk'],['Θ(?=[α-ω])','Th'],['Χ(?=[α-ω])','X'],['Ψ(?=[α-ω])','Ps'],
                     ['Αυ','Av'],['Ευ','Ev'],['Ηυ','If'],['Μπ','Mp'],
                     ['ΓΧ', 'NCH'],['ΑΥ(?=[ΘΚΞΠΣΤΦΧΨ])','AF'],['ΕΥ(?=[ΘΚΞΠΣΤΦΧΨ|\s|$])','EF'], ['ΕΎ(?=[ΘΚΞΠΣΤΦΧΨ|\s|$])','EF'],
                     ['ΗΥ(?=[ΘΚΞΠΣΤΦΧΨ|\s|$])','IF'],['(?=^|\s|$)ΜΠ','B'],['ΜΠ(?=^|\s|$)','B'],
                     ['ΑΙ','AI'],['ΟΙ','OI'],['ΟΥ','OU'],['ΟΎ', 'OU'],['ΕΙ','EI'],['ΝΤ','NT'],['ΤΣ','TS'],
                     ['ΤΖ','TZ'],['ΓΓ','NG'],['ΓΚ','GK'],['Θ(?=[Α-Ω|\s|$])','TH'],['Χ(?=[Α-Ω|\s|$])','X'],['Ψ(?=[Α-Ω|\s|$])','PS'],
                     ['ΑΥ','AV'],['ΕΥ','EV'],['ΗΥ','IF'],['ΜΠ','B']
                    ]

        for i in range(len(syllables)):
            text = re.sub(syllables[i][0],syllables[i][1],text)

        for key in translation_dictionary:
            text = re.sub(key,translation_dictionary[key],text)

        return text
    
    
    def is_greek_char(self,char):
        # Greek Unicode ranges
        return '\u0370' <= char <= '\u03FF' or '\u1F00' <= char <= '\u1FFF'

    def is_english_char(self,char):
        # English Unicode ranges
        return '\u0020' <= char <= '\u007E' or '\u0080' <= char <= '\u00FF'

    def is_greek(self,text):
        return any(GreekLang().is_greek_char(char) for char in text)

    def is_english(self,text):
        return any(GreekLang().is_english_char(char) for char in text)
    
    
