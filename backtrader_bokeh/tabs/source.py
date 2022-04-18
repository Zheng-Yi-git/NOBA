import inspect

from bokeh.models import Div, Paragraph
from bokeh.layouts import column

from ..tab import BacktraderBokehTab


class SourceTab(BacktraderBokehTab):

    def _is_useable(self):
        return not self._app.is_iplot()

    def _getSource(self):
        try:
            text = inspect.getsource(
                self._figurepage.strategy.__class__)
        except Exception:
            text = ''
        return text

    def _get_panel(self):
        title = Paragraph(
            text='Source Code',
            css_classes=['panel-title'])
        child = column(
            [title,
             Div(text=self._getSource(),
                 css_classes=['source-pre'],
                 sizing_mode='stretch_width')],
            sizing_mode='stretch_width')
        return child, 'Source Code'
