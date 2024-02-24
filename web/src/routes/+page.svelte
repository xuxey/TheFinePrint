<script lang="ts">
	import Icon from '@iconify/svelte';
	import ImageUpload from '../lib/components/imageUpload.svelte';
</script>

<span class="flex flex-col md:flex-row h-screen items-center -mt-28 py-20">
	<div class="flex flex-col w-2/3">
		<span class="flex flex-row text-6xl font-sans gap-4">
			Take Control Of Your
			<div class="text-blue-700">Privacy</div>
		</span>
		<div class="mt-3 text-2xl">
			Until now, long drawn out legal documents to keep you in the dark.
			<br />
			<br />
			With
			<span class="font-cursive text-4xl text-blue-900">the fine print</span>, understand what
			you're signing up for with on-demand AI Assisted summaries and warnings.
			<br />
		</div>
	</div>
	<img
		src="/assets/contract.svg"
		alt="Man having trouble reading a huge contract"
		class="h-2/3 aspect-auto"
	/>
</span>
<div class="pb-20 pt-28" id="how-it-works">
	<h2 class="text-4xl font-serif mb-4 -mt-20">How It Works</h2>
	<div class="flex flex-col gap-10">
		<div class="w-2/3">
			<h2 class="text-2xl text-blue-700">
				Step 1: Encounter a long, hard to understand <u>legal document</u>
			</h2>
			<p class="text-lg mt-2">
				This shouldn't be very difficult. Most companies, landlords, services, websites and
				everything else have standard contracts you are bound to.
			</p>
		</div>
		<div class="w-2/3 self-end">
			<h2 class="text-2xl text-blue-900">
				Step 2: Relax, because you have <span class="text-4xl font-cursive">The Fine Print</span>
			</h2>
			<p class="text-lg mt-2">
				Use our Firefox extension to quickly summarize and find important clauses in the document.
				<br />
				Alternatively, use our PDF or image upload features to quickly upload a document or screenshot.
			</p>
		</div>
		<div class="w-2/3">
			<h2 class="text-2xl text-blue-950">
				Step 3: Take a few seconds to read the beautiful, summarized version of your contract.
			</h2>
			<p class="text-lg mt-2">
				Use our Firefox extension to quickly summarize and find important clauses in the document.
				<br />
				Alternatively, use our PDF or image upload features to quickly upload a document or screenshot.
			</p>
		</div>
	</div>
</div>

<div id="traps" class="pb-20">
	<h2 class="text-4xl font-serif mb-4">Common Booby Traps</h2>
	<div class="flex flex-col gap-10">
		<div class="flex-row">
			<div class="w-2/3 flex flex-col">
				<h2 class="text-2xl text-blue-700">Arbitration Agreement</h2>
				<p class="text-lg mt-2">
					A legal agreement in which you agree to resolve disputes via a third-party decision-maker,
					called an arbitrator, who hears both sides and renders a binding resolution. It's often
					less formal and faster than traditional litigation, but relinquishes the right to a court
					trial.
				</p>
			</div>
		</div>
		<div class="flex flex-row justify-between items-center">
			<img src="assets/personal-info.svg" alt="" class="w-1/4" />
			<div class="w-2/3">
				<h2 class="text-2xl text-blue-900">Waiver</h2>
				<p class="text-lg mt-2">
					Legal contracts where you acknowledge the risks of an activity or event and relinquish
					your right to hold another party liable for injuries or damages arising from
					participation. They are commonly used in sports, recreational activities, and certain
					business activities to limit liability exposure.
				</p>
			</div>
		</div>
		<div class="w-2/3">
			<h2 class="text-2xl text-blue-950">Hidden Fees</h2>
			<p class="text-lg mt-2">
				Hidden fees are additional charges not disclosed upfront, often discovered later, adding
				unexpected costs. They can be in various industries like banking, airlines, and
				telecommunications, making it crucial to scrutinize contracts and understand terms to avoid
				surprise expenses.
			</p>
		</div>
		<h2 class="text-right text-3xl">Avoid these surprises, and more.</h2>
	</div>
</div>
