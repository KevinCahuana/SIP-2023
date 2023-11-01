// Actualiza los gráficos de tweets en tiempo real
function updateGraphs() {
    // Obtiene los tweets más recientes
    var tweets = getTweets();
  
    // Actualiza los gráficos con los tweets más recientes
    updatePieChart(tweets);
    updateLineChart(tweets);
  }
  
  // Filtra los tweets
  function filterTweets() {
    // Obtiene el rango de fechas seleccionado
    var startDate = $("#startDate").val();
    var endDate = $("#endDate").val();
  
    // Obtiene el tipo de sentimiento seleccionado
    var sentiment = $("#sentiment").val();
  
    // Filtra los tweets según el rango de fechas y el tipo de sentimiento
    var filteredTweets = tweets.filter(function(tweet) {
      return tweet.createdAt >= startDate && tweet.createdAt <= endDate && tweet.sentiment === sentiment;
    });
  
    // Actualiza los gráficos con los tweets filtrados
    updateGraphs(filteredTweets);
  }
  
  // Muestra un mensaje de error
  function showError(message) {
    var alert = $("#errorAlert");
    alert.text(message);
    alert.show();
  }
  
  // Oculta un mensaje de error
  function hideError() {
    var alert = $("#errorAlert");
    alert.hide();
  }
  
  // Inicializa la aplicación
  $(document).ready(function() {
    // Actualiza los gráficos de tweets por primera vez
    updateGraphs();
  
    // Agrega un listener al botón de filtrar tweets
    $("#filterButton").click(function() {
      filterTweets();
    });
  });
  