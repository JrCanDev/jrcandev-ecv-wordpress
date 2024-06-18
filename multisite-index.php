<?php
/*
Plugin Name: Multisite Index
Description: Generates an index page listing all subsites.
Version: 1.0
Author: Your Name
*/

// Hook into 'wp_loaded' to create/update the index page
add_action('wp_loaded', 'generate_multisite_index');

function generate_multisite_index() {
    if (is_main_site()) {
        $index_page_slug = 'index-of-ecvs';
        $index_page_title = 'Index of eCVs';

        // Check if the page exists
        $index_page = get_page_by_path($index_page_slug);

        if (!$index_page) {
            // Create the page if it doesn't exist
            $index_page_id = wp_insert_post(array(
                'post_title' => $index_page_title,
                'post_name' => $index_page_slug,
                'post_status' => 'publish',
                'post_type' => 'page',
                'post_content' => '',
            ));
        } else {
            $index_page_id = $index_page->ID;
        }

        // Get all sites in the network
        $sites = get_sites(array('public' => 1));

        // Generate the content for the index page
        $content = '<ul>';
        foreach ($sites as $site) {
            switch_to_blog($site->blog_id);
            $site_name = get_bloginfo('name');
            $site_url = get_home_url();
            restore_current_blog();
            $content .= "<li><a href='{$site_url}'>{$site_name}</a></li>";
        }
        $content .= '</ul>';

        // Update the page content
        wp_update_post(array(
            'ID' => $index_page_id,
            'post_content' => $content,
        ));
    }
}
