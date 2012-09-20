<?php require_once("nbbc/nbbc.php");
 $bbcode = new BBCode;
 $bbcode->SetSmileyDir('./markitup/sets/bbcode/parser/nbbc/smileys');
 $bbcode->SetSmileyURL('./markitup/sets/bbcode/parser/nbbc/smileys');
 print $bbcode->Parse($_REQUEST['data']);
 ?>
