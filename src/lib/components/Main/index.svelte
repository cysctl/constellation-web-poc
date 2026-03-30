<script lang="ts">
	import { Satellite } from '@lucide/svelte';
	import SatelliteTable from './satellite-table.svelte';
	import { satelliteStore } from '$lib/stores/satellites.svelte';
</script>

<main class="flex-1">
	<span
		class="inline-flex items-center gap-2 text-sm font-semibold text-muted-foreground uppercase select-none"
	>
		<Satellite size={18} />
		<span>satellites ({satelliteStore.list.length})</span>
	</span>

	<SatelliteTable />
</main>
