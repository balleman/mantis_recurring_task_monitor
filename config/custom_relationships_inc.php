<?php
	$g_relationships[ BUG_CUSTOM_RELATIONSHIP_INSTANCE_OF ] = array(
		'#forward' => true,
		'#complementary' => BUG_CUSTOM_RELATIONSHIP_HAS_INSTANCE,
		'#name' => 'instance-of',
		'#description' => 'rel_instance_of',
		'#notify_added' => 'email_notification_title_for_action_instance_of_relationship_added',
		'#notify_deleted' => 'email_notification_title_for_action_instance_of_relationship_deleted',
		'#edge_style' => array ( 'style' => 'dashed', 'color' => '808080' ),
	);
 
	$g_relationships[ BUG_CUSTOM_RELATIONSHIP_HAS_INSTANCE ] = array(
		'#forward' => false,
		'#complementary' => BUG_CUSTOM_RELATIONSHIP_INSTANCE_OF,
		'#name' => 'has-instance',
		'#description' => 'rel_has_instance',
		'#notify_added' => 'email_notification_title_for_action_has_instance_relationship_added',
		'#notify_deleted' => 'email_notification_title_for_action_has_instance_relationship_deleted',
		'#edge_style' => array ( 'style' => 'dashed', 'color' => '808080' ),
	);
?>
