import { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import '../App.css'

const languages = [
  { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  { code: 'ky', name: 'Кыргызча', flag: '🇰🇬' },
  { code: 'en', name: 'English', flag: '🇬🇧' },
]

function LanguageSwitcher() {
  const { i18n } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng)
    localStorage.setItem('language', lng)
    setIsOpen(false)
  }

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0]

  // Закрытие dropdown при клике вне его
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  return (
    <div className="language-dropdown" ref={dropdownRef}>
      <button
        className="language-dropdown-toggle"
        onClick={() => setIsOpen(!isOpen)}
        type="button"
      >
        <span style={{ fontSize: '1.1rem', marginRight: '0.5rem' }}>{currentLanguage.flag}</span>
        <span style={{ fontSize: '0.875rem' }}>{currentLanguage.code.toUpperCase()}</span>
        <span style={{ marginLeft: '0.5rem', fontSize: '0.75rem' }}>▼</span>
      </button>
      
      {isOpen && (
        <div className="language-dropdown-menu">
          {languages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => changeLanguage(lang.code)}
              className={`language-dropdown-item ${i18n.language === lang.code ? 'active' : ''}`}
              type="button"
              style={{
                backgroundColor: i18n.language === lang.code ? 'rgba(122, 62, 111, 0.15)' : '#ffffff',
                color: i18n.language === lang.code ? '#7A3E6F' : '#1a1a1a',
                fontWeight: i18n.language === lang.code ? 600 : 400,
              }}
            >
              <span style={{ fontSize: '1.1rem', marginRight: '0.5rem' }}>{lang.flag}</span>
              <span style={{ color: 'inherit' }}>{lang.name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default LanguageSwitcher
