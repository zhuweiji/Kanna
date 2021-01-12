from difflib import SequenceMatcher


class ReportAnalyser():
    def __init__(self, script_text: str, script_flags: list, audioobj_text: str):
        print('runnning analysis')
        self.script = script_text
        self.transcript = audioobj_text
        self.script_flags = script_flags

        print("script: ", self.script)
        print("transcript: ", self.transcript)

        self.highlighted_words = self.get_highlights()

        print("highlights: ", self.highlighted_words)
        self._output = {}

        self.evaluate_similarity_index()
        self.evaluate_keywords_hit()

    def evaluate_similarity_index(self):
        """ placeholder similarity comparison"""
        raw_output = SequenceMatcher(None, self.script, self.transcript).ratio()
        output = str(round(raw_output * 10/8 * 100 ,3)) + "%"  # result can be considered good match at 80%
        self.output['similarity'] = output

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

    @property
    def output(self) -> {str: any}:
        return self._output
