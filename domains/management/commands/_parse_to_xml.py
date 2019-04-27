import re, os
"""
<?xml version="1.0" encoding="UTF-8"?>
<Annotations start="0" num="2" total="2">
  <Annotation about="*.tutorial.djangogirls.org/*" score="0.895302">
    <Label name="_cse_e3hycfajgt0"/>
    <AdditionalData attribute="original_url" value="*.tutorial.djangogirls.org/*"/>
  </Annotation>
  <Annotation about="*.stackoverflow.com/*" score="1.0">
    <Label name="_cse_e3hycfajgt0"/>
    <AdditionalData attribute="original_url" value="*.stackoverflow.com/*"/>
  </Annotation>
</Annotations>
"""


class Parser(object):
    root_template = '''<?xml version="1.0" encoding="UTF-8"?>
<Annotations>
{annotations}
</Annotations> 
    '''
    annotation_template = '''   <Annotation about="{about}" score="{score}">
            <Label name="{label}"/>
            <AdditionalData attribute="original_url" value="{url_value}"/>
        </Annotation>'''

    def __init__(self, label):
        super().__init__()
        self.label = label
        self.annotations = None

    def parse(self, data: dict) -> None:
        self.annotations = [
            self.annotation_template.format(
                about='*.{}/*'.format(re.sub('^www.', '', key)),
                score='{:1.6f}'.format(data[key]),
                url_value=key,
                label=self.label
            )
            for key in data.keys()
        ]

    def write_file(self, file: str = os.path.join(os.getcwd(), 'annotations.xml')) -> str:
        final_annotations = self.root_template.format(
            annotations='\n'.join(self.annotations)
        )
        with open(file, 'w+') as file:
            file.write(final_annotations)
        return final_annotations
