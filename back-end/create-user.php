<?php

require_once 'db.php';

$name = '';
$email = '';
$password = md5('123465');

if (empty($name) || empty($email) || empty($password)) {
    $data = array(
        'type' => 'error',
        'message' => 'Campo(s) obrigatório(s) não preenchido(s).'
    );
} else {

    try {
        $sql = "insert into user values (null, ?, ?, ?)";
        $sql = DB::prepare($sql);
        $sql->execute([$name, $email, $password]);

        $data = array(
            'type' => 'success',
            'message' => 'Cadastro realizado com sucesso!'
        );
    } catch (PDOException $e) {
        $data = array(
            'type' => 'error',
            'message' => 'Falha ao realizar o cadastro.'
        );
    }
}

echo json_encode($data)

?>