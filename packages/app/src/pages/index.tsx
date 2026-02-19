import words from '@flashcards/data/words.json';
import { useEffect, useState } from 'react';

export type FlashCard = {
	language: string;
	front: string; // Language word
	back: string; // English word
};

const FlashCardsPage = () => {
	const [language, setLanguage] = useState('spanish'); // default language
	const [currentIndex, setCurrentIndex] = useState(0);
	const [flipped, setFlipped] = useState(false);
	const [shuffledCards, setShuffledCards] = useState<FlashCard[]>([]);

	useEffect(() => {
		// Wrap in a microtask to avoid cascading renders
		const timeout = setTimeout(() => {
			setShuffledCards(
				[...(words as FlashCard[]).filter((w) => w.language === language)].sort(
					() => Math.random() - 0.5,
				),
			);
			setCurrentIndex(0);
			setFlipped(false);
		}, 0);

		return () => clearTimeout(timeout);
	}, [language]);

	const nextCard = () => {
		setFlipped(false);
		setCurrentIndex((prev) => (prev + 1) % shuffledCards.length);
	};

	const prevCard = () => {
		setFlipped(false);
		setCurrentIndex(
			(prev) => (prev - 1 + shuffledCards.length) % shuffledCards.length,
		);
	};

	const flipCard = () => setFlipped((prev) => !prev);

	// Keyboard events
	useEffect(() => {
		const handleKeyDown = (e: KeyboardEvent) => {
			if (e.code === 'ArrowRight') nextCard();
			if (e.code === 'ArrowLeft') prevCard();
			if (e.code === 'Space' || e.code === 'Enter') {
				e.preventDefault();
				flipCard();
			}
		};
		window.addEventListener('keydown', handleKeyDown);
		return () => window.removeEventListener('keydown', handleKeyDown);
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [shuffledCards]);

	const currentCard = shuffledCards[currentIndex];

	// Handle empty flashcards
	if (shuffledCards.length === 0) {
		return (
			<div className="bg-base-200 flex min-h-screen flex-col">
				<div className="flex grow flex-col items-center justify-center p-6">
					<h1 className="mb-8 text-4xl font-bold">Flash Cards</h1>
					<p className="text-gray-500">
						No flashcards available for {language}.
					</p>
					<select
						value={language}
						onChange={(e) => setLanguage(e.target.value)}
						className="select select-bordered mt-4 capitalize">
						{[...new Set((words as FlashCard[]).map((w) => w.language))].map(
							(lang) => (
								<option key={lang} value={lang}>
									{lang}
								</option>
							),
						)}
					</select>
				</div>
			</div>
		);
	}

	return (
		<div className="bg-base-200 flex min-h-screen flex-col">
			<div className="flex grow flex-col items-center justify-center p-6">
				<h1 className="mb-8 text-4xl font-bold">Flash Cards</h1>

				{/* Language selector */}
				<select
					value={language}
					onChange={(e) => setLanguage(e.target.value)}
					className="select select-bordered mb-6 capitalize">
					{[...new Set((words as FlashCard[]).map((w) => w.language))].map(
						(lang) => (
							<option key={lang} value={lang}>
								{lang}
							</option>
						),
					)}
				</select>

				{/* Flash card */}
				<div
					className={`card bg-base-100 transform-style-3d flex h-56 w-96 cursor-pointer items-center justify-center p-4 text-center shadow-xl transition-transform duration-500 ${
						flipped ? 'rotate-y-180' : ''
					}`}
					onClick={flipCard}>
					<div className="card-body relative h-full w-full">
						<div
							className={`absolute inset-0 transition-opacity duration-500 backface-hidden ${flipped ? 'opacity-0' : 'opacity-100'}`}>
							<p className="flex h-full items-center justify-center text-2xl font-semibold">
								{currentCard.front}
							</p>
						</div>
						<div
							className={`absolute inset-0 transition-opacity duration-500 backface-hidden ${flipped ? 'opacity-100' : 'opacity-0'}`}>
							<p className="flex h-full rotate-y-180 items-center justify-center text-2xl font-semibold">
								{currentCard.back}
							</p>
						</div>
					</div>
				</div>

				{/* Navigation buttons */}
				<div className="mt-6 flex gap-4">
					<button className="btn btn-outline" onClick={prevCard}>
						Previous
					</button>
					<button className="btn btn-primary" onClick={nextCard}>
						Next
					</button>
				</div>

				<p className="mt-4 text-gray-500">
					Card {currentIndex + 1} of {shuffledCards.length}
				</p>

				<p className="mt-2 text-sm text-gray-400">
					Use ← / → to navigate, Space / Enter to flip
				</p>
			</div>
		</div>
	);
};

export default FlashCardsPage;
