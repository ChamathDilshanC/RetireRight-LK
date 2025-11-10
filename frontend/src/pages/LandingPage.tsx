/**
 * Modern Landing Page for RetireRight LK
 */
import {
  ArrowRight,
  BarChart3,
  Calculator,
  CheckCircle2,
  Shield,
  Sparkles,
  TrendingUp,
  Users,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md z-50 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <Calculator className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                RetireRight LK
              </span>
            </div>
            <button
              onClick={() => navigate('/login')}
              className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg font-medium hover:shadow-lg hover:scale-105 transition-all duration-200"
            >
              Sign In
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-8">
              <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-100 rounded-full">
                <Sparkles className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium text-blue-600">
                  Plan Your Retirement with Confidence
                </span>
              </div>

              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Calculate Your{' '}
                <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  EPF & ETF
                </span>{' '}
                Benefits
              </h1>

              <p className="text-xl text-gray-600 leading-relaxed">
                Sri Lanka's most accurate retirement calculator. Get instant
                projections of your EPF and ETF benefits with our advanced
                calculation engine.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={() => navigate('/login')}
                  className="group px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-2xl hover:scale-105 transition-all duration-300 flex items-center justify-center space-x-2"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>

                <button className="px-8 py-4 bg-white text-gray-700 rounded-xl font-semibold hover:shadow-lg transition-all duration-200 border-2 border-gray-200">
                  Watch Demo
                </button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8">
                <div>
                  <div className="text-3xl font-bold text-gray-900">10K+</div>
                  <div className="text-sm text-gray-600">Active Users</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">99.9%</div>
                  <div className="text-sm text-gray-600">Accuracy</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900">24/7</div>
                  <div className="text-sm text-gray-600">Available</div>
                </div>
              </div>
            </div>

            {/* Right Content - Illustration */}
            <div className="relative">
              <div className="relative z-10">
                {/* Floating Card 1 */}
                <div className="absolute top-0 right-0 bg-white rounded-2xl shadow-2xl p-6 transform hover:scale-105 transition-transform duration-300">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <div className="text-sm text-gray-600">EPF Balance</div>
                      <div className="text-2xl font-bold text-gray-900">
                        Rs. 2.5M
                      </div>
                    </div>
                  </div>
                </div>

                {/* Floating Card 2 */}
                <div className="absolute bottom-20 left-0 bg-white rounded-2xl shadow-2xl p-6 transform hover:scale-105 transition-transform duration-300">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
                      <Shield className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <div className="text-sm text-gray-600">
                        Retirement Age
                      </div>
                      <div className="text-2xl font-bold text-gray-900">
                        60 Years
                      </div>
                    </div>
                  </div>
                </div>

                {/* Main Card */}
                <div className="mt-20 ml-10 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-3xl p-8 shadow-2xl">
                  <div className="space-y-6">
                    <div className="flex items-center justify-between">
                      <h3 className="text-xl font-bold text-white">
                        Your Projection
                      </h3>
                      <BarChart3 className="w-6 h-6 text-white/80" />
                    </div>
                    <div className="space-y-4">
                      {[85, 70, 95].map((value, idx) => (
                        <div key={idx} className="space-y-2">
                          <div className="flex justify-between text-sm text-white/80">
                            <span>Year {2025 + idx * 5}</span>
                            <span>{value}%</span>
                          </div>
                          <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-white rounded-full transition-all duration-1000"
                              style={{ width: `${value}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Background Decoration */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-200/30 to-indigo-200/30 blur-3xl -z-10" />
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl font-bold text-gray-900">
              Everything You Need to Plan Your Retirement
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Comprehensive tools and insights to help you make informed
              decisions about your financial future
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Calculator,
                title: 'Accurate Calculations',
                description:
                  'Precise EPF & ETF calculations based on Sri Lankan regulations and latest interest rates',
                color: 'blue',
              },
              {
                icon: TrendingUp,
                title: 'Future Projections',
                description:
                  'Visualize your retirement savings growth with detailed year-by-year projections',
                color: 'green',
              },
              {
                icon: Shield,
                title: 'Secure & Private',
                description:
                  'Your financial data is encrypted and never shared. Complete privacy guaranteed',
                color: 'purple',
              },
              {
                icon: BarChart3,
                title: 'Interactive Charts',
                description:
                  'Beautiful visualizations to understand your retirement savings at a glance',
                color: 'indigo',
              },
              {
                icon: Users,
                title: 'Multiple Scenarios',
                description:
                  'Compare different retirement scenarios and make the best choice for your future',
                color: 'pink',
              },
              {
                icon: CheckCircle2,
                title: 'Real-time Updates',
                description:
                  'Stay updated with the latest EPF rates and policy changes automatically',
                color: 'orange',
              },
            ].map((feature, idx) => (
              <div
                key={idx}
                className="group p-8 bg-gray-50 rounded-2xl hover:bg-white hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-gray-200"
              >
                <div
                  className={`w-14 h-14 bg-${feature.color}-100 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}
                >
                  <feature.icon
                    className={`w-7 h-7 text-${feature.color}-600`}
                  />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-600 to-indigo-600">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="text-4xl lg:text-5xl font-bold text-white">
            Ready to Secure Your Retirement?
          </h2>
          <p className="text-xl text-blue-100">
            Join thousands of Sri Lankans who are already planning their
            financial future with confidence
          </p>
          <button
            onClick={() => navigate('/login')}
            className="group px-10 py-5 bg-white text-blue-600 rounded-xl font-bold text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300 inline-flex items-center space-x-2"
          >
            <span>Start Calculating Now</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 sm:px-6 lg:px-8 bg-gray-900">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <Calculator className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">
                RetireRight LK
              </span>
            </div>
            <p className="text-gray-400 text-sm">
              © 2025 RetireRight LK. All rights reserved.
            </p>
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <a href="#" className="hover:text-white transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Terms of Service
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};
