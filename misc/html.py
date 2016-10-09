import StringIO
from volatility.renderers.basic import Renderer

try:
    import ujson as json
except ImportError:
    import json

__author__ = 'mike'
# additional author Tran Vien Ha

class HTMLRenderer(Renderer):

    def __init__(self):
        pass

    def render(self, outfd, data):
        """Renders the treegrid to HTML"""
        print (data)
        if data.max_depth() > 1:
            json = StringIO.StringIO()
            TreeTableRenderer().render(json, data)
            outfd.write("""<html>
							<head>
							<meta charset="utf-8">
    						<title>Volatility</title>
    							<link rel="stylesheet" href="http://ludo.cubicphuse.nl/jquery-treetable/css/screen.css" media="screen" />
    							<link rel="stylesheet" href="http://ludo.cubicphuse.nl/jquery-treetable/css/jquery.treetable.css" />
    							<link rel="stylesheet" href="http://ludo.cubicphuse.nl/jquery-treetable/css/jquery.treetable.theme.default.css" />
								<script src="http://ludo.cubicphuse.nl/jquery-treetable/bower_components/jquery/dist/jquery.js"></script>
    							<script src="http://ludo.cubicphuse.nl/jquery-treetable/bower_components/jquery-ui/ui/jquery.ui.core.js"></script>
    							<script src="http://ludo.cubicphuse.nl/jquery-treetable/bower_components/jquery-ui/ui/jquery.ui.widget.js"></script>
    							<script src="http://ludo.cubicphuse.nl/jquery-treetable/bower_components/jquery-ui/ui/jquery.ui.mouse.js"></script>
    							<script src="http://ludo.cubicphuse.nl/jquery-treetable/bower_components/jquery-ui/ui/jquery.ui.draggable.js"></script>
    							<script src="http://ludo.cubicphuse.nl/jquery-treetable/bower_components/jquery-ui/ui/jquery.ui.droppable.js"></script>
    							<script src="http://ludo.cubicphuse.nl/jquery-treetable/jquery.treetable.js"></script>
							</head>
							<body>""" + json.getvalue() + """;
								<script>
									 $("#treetable").treetable({ expandable: true });
									// Highlight selected row
      								$("#treetable").on("mousedown", "tr", function() {
        							$(".selected").not(this).removeClass("selected");
        							$(this).toggleClass("selected");
      								});
								</script>
							</body>
							</html>""")
        else:
            column_titles = ", \n".join(["{ \"title\": \"" + column.name + "\"}" for column in data.columns])
            json = StringIO.StringIO()
            JSONRenderer().render(json, data)
            outfd.write("""<html>
                           <head>
                             <link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.2/css/jquery.dataTables.css">
                             <script type="text/javascript" language="javascript" src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
                             <script type="text/javascript" language="javascript" src="http://cdn.datatables.net/1.10.2/js/jquery.dataTables.min.js"></script>
                             <script type="text/javascript" class="init">
                               var dataSet = """ + json.getvalue() + """;
                               $(document).ready(function() {
                                 $('#page').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="data"></table>' );
                                 $('#data').dataTable( {
                                             "data": dataSet['rows'],
                                             "columns": [""" + column_titles + """]
                                 } );
                               } );

                              </script>
                           </head>
                           <body><div id="page"></div></body></html>""" + "\n")

class JSONRenderer(Renderer):
    def render_row(self, node, accumulator):
        return accumulator + [node.values]

    def render(self, outfd, data):
        """Renderers a treegrid as columns/row items in JSON format"""
        # TODO: Implement tree structure in JSON
        if data.max_depth() > 1:
            raise NotImplementedError("JSON output for trees has not yet been implemented")
        # TODO: Output (basic) type information in JSON
        json_input = {"columns": [column.name for column in data.columns], "rows": data.visit(None, self.render_row, [])}
        return outfd.write(json.dumps(json_input))

class TreeTableRenderer(Renderer):
    def render_row(self, node, accumulator):
        return accumulator + [node.values]

    def render(self, outfd, data):
        """Renderers a treegrid as treetable in HTML format"""
        treetable = []
        if data.max_depth() > 1:
            treetable.append("""<table id="treetable">""")
            treetable.append("""<caption>
				<a href="#" onclick="jQuery('#treetable').treetable('expandAll'); return false;">Expand all</a>
				<a href="#" onclick="jQuery('#treetable').treetable('collapseAll'); return false;">Collapse all</a>
			</caption>""")
            treetable.append("<thead>")
            treetable.append("<tr>")
            for h in data.RowStructure._fields:
                treetable.append("<th>")
                treetable.append(h)
                treetable.append("</th>")
            treetable.append("</tr>")
            treetable.append("</thead>")
            treetable.append("<tbody>")
            for p in data.visit(None, self.render_row, []):
                treetable.append("<tr data-tt-id='")
                treetable.append(str(p.pid))
                treetable.append("' data-tt-parent-id='")
                treetable.append(str(p.ppid))
                treetable.append("'>")
                for i in range (0,len(p)):
                    treetable.append("<td>")
                    treetable.append(str(p[i]))
                    treetable.append("</td>")
                treetable.append("</tr>")	
            treetable.append("</tbody>")
            treetable.append("</table>")

        return outfd.write("".join(treetable))
