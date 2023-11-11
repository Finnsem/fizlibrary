let idleTime = 0;

function resetIdleTime() {
    idleTime = 0;
}

function checkIdleTime() {
    idleTime++;
    if (idleTime >= 5) {  // 5 minutes
        window.location.href = "{{ url_for('logout') }}";
    }
}

window.onload = function() {
    // Reset idle time on mouse movement, keypress, or touch
    document.onmousemove = resetIdleTime;
    document.onkeypress = resetIdleTime;
    document.ontouchstart = resetIdleTime;

    // Check idle time every minute
    setInterval(checkIdleTime, 60000); // 60000 milliseconds = 1 minute
};