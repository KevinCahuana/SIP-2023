
var pie_chart_d="{{pie_chart_data}}"
var correctedString1 = pie_chart_d.replace(/&#34;/g, '"');
var pie_chart_data = JSON.parse(correctedString1); // The JSON object as a string
var line_chart_d="{{line_chart_data}}"
var correctedString2 = line_chart_d.replace(/&#34;/g, '"');
var line_chart_data = JSON.parse(correctedString2); // The JSON object as a string
//var pie_chart_data = JSON.parse('{"datasets": [ {"data": [5, 9, 8] } ] ,"labels": ["Positivos", "Negativos", "Neutros"] }'); // The JSON object as a string
//var line_chart_data = JSON.parse('{"labels": ["2023-11-09", "2023-11-10"], "datasets": [{"label": "Positivos", "data": [0, 5]}, {"label": "Negativos", "data": [0, 9]}, {"label": "Neutros", "data": [1, 7]}]}'); // The JSON object as a string

var pieChart = new Chart(document.getElementById('pie-chart'), {
    type: 'pie',
    data: pie_chart_data,
});

var lineChart = new Chart(document.getElementById('line-chart'), {
    type: 'line',
    data: line_chart_data,
});
