<?php

use Illuminate\Support\Facades\Route;

Route::get('/help', function () {
    return view('welcome');
});


Route::get('/', function () {
    return view('home');
});



