<?php /* index.php ( lilURL implementation ) */

require_once 'includes/conf.php'; // <- site-specific settings
require_once 'includes/hjurl.php'; // <- lilURL class file

$lilurl = new lilURL();
$msg = '';
$id = '';
$location = -1;

if ( isSet($_GET['id']) ) // check GET first
{
        $id = mysql_escape_string($_GET['id']);
	        $location = $lilurl->get_url($id);
		}

// if the location isn't empty, redirect to it's url
if ( $location != -1)
{
   header('Location: '.$location);
   }
   else
   {
           $msg = '<p class="error">Sorry, but that lil&#180; URL isn\'t in our database.</p>';
	   }


?>

<html>
  <?php echo $msg; ?>
 </html>
  