<?php
date_default_timezone_set('Africa/Cairo');
header('Content-Type: application/json');
include 'db_connection.php';

if (isset($_GET['turbidity_value']) && isset($_GET['ph_value'])) {
    $turbidity = $_GET['turbidity'];
    $ph_value = $_GET['ph_value'];

    $date = date('Y-m-d h:i:s');
    $insert = "INSERT INTO water_app_waterdata(`datetime`,turbidity_value,ph_value)  VALUES('$date','$turbidity_value','$ph_value')";
    $sql = $db->query($insert);

    if ($sql == true) {
        $response = array(
            "message" => "Data saved successfully",
            "status" => 200
        );
    } else {
        $response = array(
            "message" => "Something went wrong",
            "status" => 500
        );
    }

    echo json_encode($response);
} else {
    $response = array(
        "message" => "Missing parameters",
        "status" => 400
    );
    echo json_encode($response);
}
?>

