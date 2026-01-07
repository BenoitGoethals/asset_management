/**
 * Sorts an HTML table by a specific column index.
 * @param {number} n - The index of the column to sort by.
 */
function sortTable(n) {
  let table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("serverTable");
  switching = true;
  dir = "asc"; // Set the sorting direction to ascending

  while (switching) {
    switching = false;
    rows = table.rows;

    // Loop through all table rows (except the first, which contains table headers)
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];

      // Get values and check if they are numbers for numeric sorting
      let xVal = x.innerHTML.toLowerCase();
      let yVal = y.innerHTML.toLowerCase();

      // Basic numeric detection (strip % or units)
      let xNum = parseFloat(xVal.replace(/[^\d.-]/g, ''));
      let yNum = parseFloat(yVal.replace(/[^\d.-]/g, ''));

      if (dir === "asc") {
        if (!isNaN(xNum) && !isNaN(yNum)) {
            if (xNum > yNum) { shouldSwitch = true; break; }
        } else if (xVal > yVal) {
          shouldSwitch = true;
          break;
        }
      } else if (dir === "desc") {
        if (!isNaN(xNum) && !isNaN(yNum)) {
            if (xNum < yNum) { shouldSwitch = true; break; }
        } else if (xVal < yVal) {
          shouldSwitch = true;
          break;
        }
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount++;
    } else {
      if (switchcount === 0 && dir === "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}