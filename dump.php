<?php

// Assuming you have a database connection
$servername = "localhost";
$username = "juhavdph_snowdog";
$password = "snowdogSalasana";
$dbname = "juhavdph_snowdog";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch data from your_table_name
$sql = "SELECT * FROM location_history order by id";
$result = $conn->query($sql);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display Data</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>

    <h2>Location history</h2>

    <?php
    if ($result->num_rows > 0) {
        echo "<table>";
        echo "<tr><th>ID</th><th>Latitude</th><th>Longitude</th><th>Altitude</th><th>Speed</th><th>Timestamp</th><th>In Area</th></tr>";

        while ($row = $result->fetch_assoc()) {
            echo "<tr>";
            echo "<td>" . $row['id'] . "</td>";
            echo "<td>" . $row['lat'] . "</td>";
            echo "<td>" . $row['lon'] . "</td>";
            echo "<td>" . $row['alt'] . "</td>";
            echo "<td>" . $row['speed'] . "</td>";
            echo "<td>" . $row['ts'] . "</td>";
            echo "<td>" . $row['in_area'] . "</td>";
            echo "</tr>";
        }

        echo "</table>";
    } else {
        echo "No data found.";
    }

    // Close the connection
    $conn->close();

    ?>

</body>
</html>
