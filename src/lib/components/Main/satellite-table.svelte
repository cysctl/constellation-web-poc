<script lang="ts">
	// This is a placeholder component for the satellite table
	// It will be replaced with actual data and functionality later
</script>

<table class="mt-5 w-full caption-bottom text-sm whitespace-nowrap">
	<thead class="border-b border-border">
		<tr
			class="text-left text-xs font-medium tracking-wider text-muted-foreground uppercase [&_th]:px-3 [&_th]:py-2"
		>
			<th>Type</th>
			<th>Name</th>
			<th class="w-[10%]">State</th>
			<th class="w-[35%]">Last Message</th>
			<th>Heartbeat</th>
			<th class="w-[8%]">Lives</th>
			<th class="w-[20%] text-right">Actions</th>
		</tr>
	</thead>
	<tbody class="divide-y divide-border [&_td]:px-3 [&_td]:py-2">
		<tr>
			<td>Sputnik</td>
			<td>Device1</td>
			<td>NEW</td>
			<td>Last message content...</td>
			<td>3000ms</td>
			<td>3</td>
		</tr>
	</tbody>
</table>
