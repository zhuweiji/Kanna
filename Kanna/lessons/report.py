from difflib import SequenceMatcher
from num2words import num2words
import re
import spacy

from typing import List

""" possible packages:
        https://github.com/Azd325/gingerit
        gingerit: API wrapper for correcting spelling and grammar mistakes based on the context of complete sentences
        
        https://github.com/atpaino/deep-text-corrector
        deep-text-corrector: ML correct grammatical errors in conversational english
        
        https://github.com/bakwc/JamSpell
        jamspell: ML spell checking
"""


class ReportAnalyser:
    def __init__(self, script_text: str, script_flags: list, audioobj_text: str):
        print('runnning analysis')

        self.script = self.get_cleaned_text(script_text)
        self.transcript = self.get_cleaned_text(audioobj_text)
        self.script_flags = script_flags
        self.highlighted_words = self.get_highlights()[:]
        self.highlights_missed = []

        self._output = {}

        self.evaluate_similarity_index()
        self.evaluate_keywords_hit()
        self.full_keyphrase_analysis()

        print("script: ", self.script)
        print("transcript: ", self.transcript)
        print("highlights: ", self.highlighted_words)

    def get_highlights(self) -> list:
        """ converts script flags to list of highlighted key phrases """
        script_text = self.script
        flags = self.script_flags

        if all(i == '0' for i in flags):
            return []

        highlights = []
        phrase = ""
        for index, word in enumerate(script_text.split(" ")):
            if flags[index] == '1':
                phrase += word + ' '
            else:
                if phrase:
                    highlights.append(phrase.strip())
                    phrase = ""
        return highlights

    def evaluate_similarity_index(self):
        """ placeholder similarity comparison"""
        transcript = self.transcript.split()
        script = self.script.split()

        seqmatch_output = SequenceMatcher(None, self.script, self.transcript).ratio()
        seqmatch_final = round(seqmatch_output * 10 / 8, 3)  # result can be considered good match at 80%
        seqmatch_final = 1 if seqmatch_final > 1 else seqmatch_final

        list1 = set(transcript)
        list2 = set(script)
        word_similiarity_output = sum(el in list1 for el in list2)/min(len(list1), len(list2))

        output = seqmatch_final * 0.6 + word_similiarity_output * 0.4

        self.output['similarity'] = str(output) + "%"
        return output

    def evaluate_keywords_hit(self) -> (int, int):
        # evaluate if all keywords are in transcript
        highlighed_set = set()
        for phrase in self.highlighted_words:
            for word in phrase.split(" "):
                highlighed_set.add(word)

        print("set: ", highlighed_set)
        highlights_hit_counter = 0
        highlights_missed = []
        for word in highlighed_set:
            if word in self.transcript:
                highlights_hit_counter += 1
            else:
                highlights_missed.append(word)

        self.output['keywords_missed'] = highlights_missed
        self.output['keywords_hit_ratio'] = f'{highlights_hit_counter}/{len(highlighed_set)}'

    def analyse_keyphrase(self, keyphrase: str) -> dict:
        """ naively find LCS of highlight within transcript """
        # todo: lcs is bugged
        transcript = self.transcript

        len_longest_subsequence = 0  # subsequence: any keyword at current position in transcript or any position after
        longest_substring = ""

        try:
            # iterate through every word, and for each word iterate through every keyword in keyphrase
            for index, word in enumerate(transcript.split(' ')):
                len_subsequence = 0  # temp variables that store lcs and lss for the current word being analysed
                temp_substring = ""

                for ext, keyword in enumerate(keyphrase.split(' ')):
                    if keyword == transcript.split(' ')[index + ext]:  # iterate through each keyword in phrase and
                        len_subsequence += 1  # compare with equivalent word in transcript
                        temp_substring += keyword
                    else:
                        if len(temp_substring) > len(longest_substring):
                            longest_substring = temp_substring
                        temp_substring = ""

                len_longest_subsequence = len_subsequence if len_subsequence > len_longest_subsequence \
                    else len_longest_subsequence  # replace the true lcs if the temp lcs is longer

        except IndexError:
            pass

        # print()
        # print()
        # print("score values")
        # print({"keyphrase": keyphrase})
        #
        # print(len_longest_subsequence,",",len(keyphrase.split()), len_longest_subsequence/len(keyphrase.split()))
        # print({
        #     "longest substr": longest_substring,
        #
        # })

        # treat lcs as more important than lss
        score = 0.3 * len_longest_subsequence / len(keyphrase.split()) \
                + 0.7 * len(longest_substring) / len(keyphrase.split())

        output = {
            "longest_substring_length": len_longest_subsequence,
            "lcs": longest_substring,
            "score": score,
        }

        return output

    def full_keyphrase_analysis(self):
        keyphrases = self.highlighted_words
        results = {}    # store outputs in dict with keys being the index of keyphrase in list, creating dict of dicts
        overall_score = 0

        for index, phrase in enumerate(keyphrases):
            results[index] = self.analyse_keyphrase(phrase)
            overall_score += self.analyse_keyphrase(phrase)['score'] / len(keyphrases)

        self.output['keyphrase_score'] = overall_score
        return overall_score

    @property
    def output(self) -> {str: any}:
        return self._output

    @staticmethod
    def get_cleaned_text(text):
        result = re.sub(r"[^a-zA-Z1-9 ]", '', text)

        _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
        result = _RE_COMBINE_WHITESPACE.sub(" ", result).strip()

        output = ""
        for word in result:
            if word.isnumeric():
                word = num2words(word)
                print(word)
            output += word

        output = output.lower()
        return output
