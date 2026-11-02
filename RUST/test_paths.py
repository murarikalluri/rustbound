"""Cross-check the browser's guided predictions against actual Rust execution."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from learning import LESSONS


class PathTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node') and shutil.which('rustc'), 'requires Node and rustc')
    def test_guided_templates_match_rust_and_topic_links_exist(self):
        root = Path(__file__).resolve().parent
        script = '''global.window = {}; global.document = {addEventListener(){}};
        require('./static/learning-paths.js');
        const {activities,preview,projects} = window.RustboundPaths;
        const cases = activities.flatMap((a,i) => {
          const values = [a.initial,a.target];
          if(a.type==='number') values.push(0,10);
          return values.map(v=>preview(i,v));
        });
        console.log(JSON.stringify({cases,ids:[...activities.map(a=>a.lesson),...projects.flatMap(p=>p.topics)]}));'''
        payload = json.loads(subprocess.check_output(['node','-e',script], cwd=root, timeout=15))
        self.assertLessEqual(set(payload['ids']), {x['id'] for x in LESSONS})
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            modules, calls, expected = [], [], []
            for i,case in enumerate(payload['cases']):
                modules.append(f"mod activity_{i} {{\n{case['code']}\npub fn run() {{ main(); }}\n}}")
                calls.append(f'println!("case {i}"); activity_{i}::run();')
                expected.extend([f'case {i}', *case['output'].splitlines()])
            source, binary = path/'guided.rs', path/'guided.exe'
            source.write_text('\n'.join(modules)+'\nfn main() {\n'+'\n'.join(calls)+'\n}', encoding='utf-8')
            subprocess.run(['rustc','--edition=2024',str(source),'-o',str(binary)], check=True, timeout=30)
            self.assertEqual(subprocess.check_output([str(binary)], text=True, timeout=5).splitlines(), expected)


if __name__ == '__main__':
    unittest.main()
