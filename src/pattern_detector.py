import os
import json
from collections import defaultdict
from datetime import datetime

class PatternDetector:
    def __init__(self, data_path="data", workflow_path="workflows"):
        self.data_path = data_path
        self.workflow_path = workflow_path
        os.makedirs(self.workflow_path, exist_ok=True)

    def load_summaries(self):
        summaries = []
        for s in sorted(os.listdir(self.data_path)):
            sp = os.path.join(self.data_path, s)
            if os.path.isdir(sp):
                f = os.path.join(sp, "summary.json")
                if os.path.exists(f):
                    try:
                        with open(f, "r", encoding="utf-8") as fh:
                            summaries.append(json.load(fh))
                    except Exception:
                        pass
        return summaries

    def detect_repetitive_actions(self, summaries):
        counter = defaultdict(int)
        for s in summaries:
            acts = s.get("detected_actions", [])
            for a in acts:
                if isinstance(a, dict):
                    k = a.get("action")
                else:
                    k = str(a)
                counter[k] += 1
        return {k:v for k,v in counter.items() if v >= 2}

    def generate_workflow_json(self, repetitive):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        wf = {"timestamp": ts, "repetitive_actions": repetitive}
        out = os.path.join(self.workflow_path, f"workflow_{ts}.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(wf, f, indent=4)
        return out

    def process(self):
        summaries = self.load_summaries()
        if not summaries:
            return None
        repetitive = self.detect_repetitive_actions(summaries)
        if not repetitive:
            return None
        return self.generate_workflow_json(repetitive)

if __name__ == "__main__":
    PatternDetector().process()