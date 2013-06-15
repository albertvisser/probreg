<%!
def ntobr(input):
    return input.replace('\\n', '<br>')
%>
<html>
<head>
% if css:
    <style>${css}</style>
% endif
    <title>${hdr}</title>
</head>
<body>
    % if lijst:
        <table>
        % for action, title, catg, started, l_wijz in lijst:
            <tr><td>${action}&nbsp;&nbsp;</td><td>${title}</td></tr>
            <tr><td>&nbsp;</td><td>${catg} gemeld op ${started}<br>${l_wijz}</td></tr>
        % endfor
        </table>
    % endif
    % if actie:
        <table>
            <tr><td>Actie:</td><td>${actie}</td></tr>
            <tr><td>Gemeld op:</td><td>${datum}</td></tr>
            <tr><td>Betreft:</td><td>${oms}</td></tr>
            <tr><td>Melding:</td><td>${tekst}</td></tr>
            <tr><td>Soort actie:</td><td>${soort}</td></tr>
            <tr><td>Status:</td><td>${status}</td></tr>
        </table>
    % endif
    % for title, text in sections:
        <hr>
        <p><b>${title}</b><br>${text | ntobr}</p>
    % endfor
    <hr>
    % for date, text in events:
        <p><b>${date}</b><br>${text | ntobr}</p>
    % endfor
</body>
</html>
