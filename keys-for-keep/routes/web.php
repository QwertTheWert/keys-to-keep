<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('mainMenu');
});
Route::get('/test', function () {
    return view('welcome');
});
