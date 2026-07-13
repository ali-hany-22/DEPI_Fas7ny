import { Star } from 'lucide-react'

export default function StarRating({ rating, size = 14 }) {
  const rounded = Math.round(rating)
  return (
    <div className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map((i) => (
        <Star
          key={i}
          size={size}
          className={i <= rounded ? 'fill-gold text-gold' : 'fill-gray-200 text-gray-200'}
        />
      ))}
    </div>
  )
}
