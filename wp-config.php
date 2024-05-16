<?php
/**
* The base configuration for WordPress
*
* The wp-config.php creation script uses this file during the
* installation. You don't have to use the web site, you can
* copy this file to "wp-config.php" and fill in the values.
*
* This file contains the following configurations:
*
* * MySQL settings
* * Secret keys
* * Database table prefix
* * ABSPATH
*
* @link https://wordpress.org/support/article/editing-wp-config-php/
*
* @package WordPress
*/
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wordpress' );

/** MySQL database password */
define( 'DB_PASSWORD', 'root' );

/** MySQL hostname */
define( 'DB_HOST', 'mysql' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
/**#@+
* Authentication Unique Keys and Salts.
*
* Change these to different unique phrases!
* You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
*
* You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
*
* @since 2.6.0
*/
define( 'AUTH_KEY',         '*@z+PO-eNnYsyC_Hpd3-X9KFz;&Al:Nohm&[ICLkU,7EXLAgRX#bRO7j~WxGnJ59' );
define( 'SECURE_AUTH_KEY',  'xo@#CI4>f-o0+Rhm?q5[;js3,V*m[!jOSSh-F>5<e#yw6UZ^p9aEp5ZZY>q|P/vk' );
define( 'LOGGED_IN_KEY',    'U4cm>|n}a6H6F+8bVa@+j$0)P>t|Q9GkvQV.>a tkTeH5t?|Iz;at+.qtn+e6Y|<' );
define( 'NONCE_KEY',        'O/xn+vfh h/D?m4b)W!#+d*YW2)WoeANCJ[5IKY0j1]!*Ul_!-BA=]WT}zzD9=> ' );
define( 'AUTH_SALT',        '>}`%:FOv?~OgGVoPSpGu^?mA0N[!y3gAI+O.Y>j|~XBE2]at#IR<Cf60=dwop1D]' );
define( 'SECURE_AUTH_SALT', '=rdO):ME?oU_~c-9G?w#^p?Nbohqp>A)ze!J.(gbtQnT*5/qShBa x@w1K6XI(4 ' );
define( 'LOGGED_IN_SALT',   'Dt@pe,4]]eo?,waOCPO.]|UjV[H|U+*(Ll<:R.< m O>.V^|->LIF}a^,n!b8S?G' );
define( 'NONCE_SALT',       '-~_ORt2u0$g2@FOo5yX;2=6K=Jt-SY[mB}|PuRc-U)+6:+^Bm|%hl/hHE7Bzg.0_' );
/**#@-*/
/**
* WordPress database table prefix.
*
* You can have multiple installations in one database if you give each
* a unique prefix. Only numbers, letters, and underscores please!
*/
$table_prefix = 'wp_';
/**
* For developers: WordPress debugging mode.
*
* Change this to true to enable the display of notices during development.
* It is strongly recommended that plugin and theme developers use WP_DEBUG
* in their development environments.
*
* For information on other constants that can be used for debugging,
* visit the documentation.
*
* @link https://wordpress.org/support/article/debugging-in-wordpress/
*/
define('WP_DEBUG', true);
/* Add any custom values between this line and the "stop editing" line. */

define ('MULTISITE', true);
define ('SUBDOMAIN_INSTALL', false);
define ('DOMAIN_CURRENT_SITE', getenv('SITE_URL'));
define ('PATH_CURRENT_SITE', '/');
define ('SITE_ID_CURRENT_SITE', 1);
define ('BLOG_ID_CURRENT_SITE', 1);

/* That's all, stop editing! Happy publishing. */

define('COOKIE_DOMAIN', '');
define('COOKIEPATH', '/');
define('SITECOOKIEPATH', '/');
define('ADMIN_COOKIE_PATH', '/');
define('COOKIEHASH', md5(getenv('SITE_URL')));

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
   define( 'ABSPATH', __DIR__ . '/' );
}
/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';