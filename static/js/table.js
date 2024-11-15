function allowDrop(event) {
    event.preventDefault();
  }

  function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
  }

  function drop(event, status) {
    event.preventDefault();
    var issueId = event.dataTransfer.getData("text");
    var issueElement = document.getElementById(issueId);
    event.target.appendChild(issueElement);

    // Make an AJAX request to update the status
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{% url 'update_issue_status' %}", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
    xhr.send("id=" + issueId + "&status=" + status);
  }