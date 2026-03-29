<script lang="ts">
	import ConnectionStatus from './connection-status.svelte';
	import HeaderButtons from './header-buttons.svelte';
	import Logo from './logo.svelte';
</script>

<header class="flex items-center justify-between py-4">
	<Logo />
	<section class="flex items-center gap-4">
		<ConnectionStatus />
		<HeaderButtons />
	</section>
</header>
