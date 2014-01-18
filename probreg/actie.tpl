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
            <tr><td>&nbsp;</td><td>${catg}
            % if started:
                gemeld op ${started}
            % endif
            - ${l_wijz}</td></tr>
        % endfor
        </table>
    % endif
    % if actie:
        <table>
            <tr><td>Actie:</td><td>&nbsp;${actie}</td></tr>
            <tr><td>Gemeld op:</td><td>&nbsp;${datum}</td></tr>
            <tr><td>Betreft:</td><td>&nbsp;${oms}</td></tr>
            <tr><td>Melding:</td><td>&nbsp;${tekst}</td></tr>
            <tr><td>Soort actie:</td><td>&nbsp;${soort}</td></tr>
            <tr><td>Status:</td><td>&nbsp;${status}</td></tr>
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
