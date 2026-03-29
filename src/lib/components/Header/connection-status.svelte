<script lang="ts">
	let connStatus: 'connected' | 'disconnected' = 'connected';
</script>

<div class="inline-flex items-center gap-2">
	<div
		class="size-2 animate-pulse rounded-full {connStatus === 'connected'
			? 'bg-state-run'
			: 'bg-red-500'}"
	></div>

	<span class="hidden text-sm lg:block">
		{connStatus === 'connected' ? 'Connected' : 'Disconnected'}
	</span>
</div>
