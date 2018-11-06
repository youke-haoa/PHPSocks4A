<?php
        class response {
               public $isSucess = false;
               public $des = "";
               public $resData = "";
        }
        $rsp = new response();
        
        $dnsIP = "8.8.4.4";
        $dnsPort = 53;
        
        
        $postData = file_get_contents("php://input"); 
        $base64decode = base64_decode($postData);
        
        $dnsSocket = socket_create(AF_INET,SOCK_DGRAM,SOL_UDP);
        $sendCount = socket_sendto(
                $dnsSocket,
                $base64decode,
                strlen($base64decode),
                0,
                $dnsIP,
                $dnsPort
        );
        socket_recvfrom(
                $dnsSocket,
                $result,
                512,
                0,
                $dnsIP,
                $dnsPort
        );
        $rsp->isSucess = true;
        $rsp->des = "sucess";
        $rsp->resData = base64_encode($result);
        
        echo json_encode($rsp);
?>

